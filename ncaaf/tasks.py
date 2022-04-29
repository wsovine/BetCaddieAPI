from botocore.errorfactory import ClientError

from ncaaf.models import TeamMappings, FantasyDataLeagueHierarchy, FantasyDataGames, FootballOutsidersFPlusRatings, \
    ArmBetCalcs
import requests
import boto3
from io import StringIO
from pycaret.classification import *
import difflib
from tqdm.auto import tqdm

from ncaaf.services import fd_base_url, fd_headers, cfbd_current_week, cfbd_bet_api


# Mapping
def load_mappings():
    """
    Mapping table is manually created and saved in data/ncaaf_mappings.csv
    It links team ID's from different sources
    """
    TeamMappings.objects.all().delete()

    s3 = boto3.client('s3')
    mapping_file = s3.get_object(Bucket='bet-caddie', Key='ncaaf/ncaaf_mappings.csv')
    body = mapping_file['Body']
    csv_string = body.read().decode('utf-8')
    df_mappings = pd.read_csv(StringIO(csv_string), sep=',')

    for idx, row in df_mappings.iterrows():
        fd_team = FantasyDataLeagueHierarchy.objects.get(TeamID=row.fd_team_id)
        try:
            fo_team = FootballOutsidersFPlusRatings.objects.get(Team=row.fo_team)
        except FootballOutsidersFPlusRatings.DoesNotExist:
            pass

        TeamMappings.objects.create(fd_team=fd_team, fo_team=fo_team, cfbd_team_id=row.cfbd_team_id)

# Fantasy Data .io
# fantasydata.io plan is restricted to 100 api calls per day, so makes
# sense to load the data into the database after the call.
def load_fd_teams():
    r = requests.get(f'{fd_base_url}LeagueHierarchy', headers=fd_headers)
    df_teams = pd.json_normalize(r.json(), 'Teams', sep='_')

    df_teams = df_teams.fillna(np.nan).replace([np.nan], [None])

    teams_dict = df_teams.to_dict(orient='records')
    model_instances = [FantasyDataLeagueHierarchy(**team) for team in teams_dict]
    FantasyDataLeagueHierarchy.objects.all().delete()
    FantasyDataLeagueHierarchy.objects.bulk_create(model_instances)


def load_fd_games(season: int = None, post_season: bool = False, week: int = None):
    if not season:
        calendar_week = cfbd_current_week()
        season = calendar_week['season']
    season_str = f'{season}POST' if post_season else str(season)

    if not week:
        r = requests.get(f'{fd_base_url}Games/{season_str}', headers=fd_headers)
    else:
        r = requests.get(f'{fd_base_url}GamesByWeek/{season_str}/{week}', headers=fd_headers)

    df_games = pd.json_normalize(r.json(), sep='_')

    if not df_games.empty:
        df_games['Day'] = pd.to_datetime(df_games['Day']).dt.date
        df_games = df_games.fillna(np.nan).replace([np.nan], [None])

        games_dict = df_games.to_dict(orient='records')
        for game in games_dict:
            away_team = FantasyDataLeagueHierarchy(TeamID=game.pop('AwayTeamID'))
            home_team = FantasyDataLeagueHierarchy(TeamID=game.pop('HomeTeamID'))
            game['AwayTeam'] = away_team
            game['HomeTeam'] = home_team
            FantasyDataGames.objects.update_or_create(**game)


# Football Outsiders
def load_fo_fplus_ratings(season: int = None, season_type: str = None, week: int = None):
    if not season:
        calendar_week = cfbd_current_week()
        season = calendar_week['season']
        season_type = calendar_week['season_type'] if not season_type else season_type
        week = calendar_week['week'] if not week else week

    s3 = boto3.client('s3')
    try:
        mapping_file = s3.get_object(
            Bucket='bet-caddie',
            Key=f'ncaaf/{season} {season_type} {week} COLLEGE FOOTBALL F+ RATINGS.csv'
        )
    except ClientError:
        mapping_file = s3.get_object(Bucket='bet-caddie', Key=f'ncaaf/{season} COLLEGE FOOTBALL F+ RATINGS.csv')

    body = mapping_file['Body']
    csv_string = body.read().decode('utf-8')
    df_fplus = pd.read_csv(StringIO(csv_string), sep=',')

    df_fplus.columns = df_fplus.columns.str.replace('+', '_plus', regex=False)
    df_fplus = df_fplus[['Team', 'F_plus', 'OF_plus', 'DF_plus', 'FEI', 'SP_plus']]
    fplus_dict = df_fplus.to_dict(orient='records')

    for ratings in fplus_dict:
        FootballOutsidersFPlusRatings.objects.update_or_create(**ratings)


# The Prediction Tracker
def load_prediction_tracker_lines(season: int, season_type: str, week: int = None):
    tqdm.pandas()

    season = int(season)
    week = int(week) if week else week

    # Load prediction tracker rating line csv from s3 bucket
    s3_resource = boto3.resource('s3')
    s3_client = boto3.client('s3')
    prediction_tracker_bucket = s3_resource.Bucket('bet-caddie')
    keys = [o.key for o in prediction_tracker_bucket.objects.filter(Prefix='ncaaf/prediction_tracker/')]
    if f'ncaaf/prediction_tracker/ncaa{season} {season_type} {week}.csv' in keys:
        mapping_file = s3_client.get_object(
            Bucket='bet-caddie',
            Key=f'ncaaf/prediction_tracker/ncaa{season} {season_type} {week}.csv'
        )
    elif f'ncaaf/prediction_tracker/ncaa{season}.csv' in keys:
        mapping_file = s3_client.get_object(
            Bucket='bet-caddie',
            Key=f'ncaaf/prediction_tracker/ncaa{season}.csv'
        )
    else:
        return None

    body = mapping_file['Body']
    csv_string = body.read().decode('utf-8')
    df_pred = pd.read_csv(StringIO(csv_string), sep=',')

    if df_pred.empty:
        return None

    # Load the Betting Lines data from CFBD
    if week:
        games = cfbd_bet_api.get_lines(year=season, season_type=season_type, week=week)
    else:
        games = cfbd_bet_api.get_lines(year=season, season_type=season_type)
    df_lines = pd.json_normalize([g.to_dict() for g in games])

    def get_line(lines, side: str):
        try:
            return [l[f'{side}Moneyline'] for l in lines if l['provider'] == 'Bovada'][0]
        except IndexError:
            return None

    df_lines['home_ml'] = df_lines.lines.apply(lambda r: get_line(r, 'home'))
    df_lines['away_ml'] = df_lines.lines.apply(lambda r: get_line(r, 'away'))

    df_lines.dropna(subset=['home_ml', 'away_ml'], axis=0, inplace=True)

    if df_lines.empty:
        return None

    # Match betting line data with prediction tracker data
    team_mapping = {
        'Massachusetts': 'UMass',
        'Miami (Fla.)': 'Miami',
        'Louisiana-Lafayette': 'Lafayette',
        'Mississippi': 'Ole Miss'
    }

    df_pred.Home = df_pred.Home.replace(team_mapping)
    df_pred.Road = df_pred.Road.replace(team_mapping)

    unmatchable = set()

    def match_team(team):
        try:
            return difflib.get_close_matches(
                team, set(df_lines.home_team.unique().tolist() + df_lines.away_team.unique().tolist())
            )[0]
        except IndexError:
            unmatchable.add(team)
            return None

    print('Matching home teams...')
    df_pred['home_join'] = df_pred.Home.progress_apply(lambda t: match_team(t))
    print('Matching away teams...')
    df_pred['away_join'] = df_pred.Road.progress_apply(lambda t: match_team(t))
    print(f'Teams that couldnt be matched: {unmatchable}')

    # Merge Dataframes
    if week:
        df = df_lines.merge(
            df_pred,
            left_on=['home_team', 'away_team'],
            right_on=['home_join', 'away_join']
        )
        df.drop_duplicates(subset=['home_team', 'away_team'], inplace=True)
    else:
        df_pred.drop(columns=['week'], inplace=True)
        df = df_lines.merge(
            df_pred,
            left_on=['home_team', 'away_team', 'home_score', 'away_score'],
            right_on=['home_join', 'away_join', 'hscore', 'vscore']
        )
        df.drop_duplicates(subset=['home_team', 'away_team', 'home_score', 'away_score'], inplace=True)
    df.drop(columns=['home_join', 'away_join'], inplace=True)

    print(df_lines.shape)
    print(df_pred.shape)
    print(df.shape)

    # Load the pycaret model
    print('Loading pycaret model from S3')
    model = load_model(
        model_name='ncaaf_arm_v3',
        platform='aws',
        authentication={
            'bucket': 'bet-caddie'
        },
        verbose=True
    )

    # Get predictions
    print('Running model predictions')
    df_model = predict_model(model, df, raw_score=True)

    # Save to database
    bet_calc_data = df_model[[
        'id', 'Score_False', 'Score_True', 'away_ml', 'home_ml'
    ]].rename(columns={
        'id': 'cfbd_game_id',
        'Score_False': 'away_ml_prob',
        'Score_True': 'home_ml_prob'
    }).to_dict(orient='records')

    return [ArmBetCalcs.objects.create(**data) for data in bet_calc_data]


# Odds API
