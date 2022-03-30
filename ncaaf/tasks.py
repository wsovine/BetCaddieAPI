import pandas as pd

from ncaaf.models import TeamMappings, FantasyDataLeagueHierarchy, FantasyDataGames, FootballOutsidersFPlusRatings
import requests
import boto3
from io import StringIO
import numpy as np

from ncaaf.services import fd_base_url, fd_headers, cfbd_current_week


# Mapping
def load_mappings():
    """
    Mapping table is manually created and saved in data/ncaaf_mappings.csv
    It links team ID's from different sources
    """
    s3 = boto3.client('s3')
    mapping_file = s3.get_object(Bucket='bet-caddie', Key='ncaaf/ncaaf_mappings.csv.csv')
    body = mapping_file['Body']
    csv_string = body.read().decode('utf-8')
    df_mappings = pd.read_csv(StringIO(csv_string), sep=',')
    mapping_dict = df_mappings.to_dict(orient='records')
    model_instances = [TeamMappings(**mapping) for mapping in mapping_dict]
    TeamMappings.objects.all().delete()
    TeamMappings.objects.bulk_create(model_instances)


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


def load_fd_games(season: int = None, post_season: bool = False):
    if not season:
        week = cfbd_current_week()
        season = week['season']
    season_str = f'{season}POST' if post_season else str(season)
    r = requests.get(f'{fd_base_url}Games/{season_str}', headers=fd_headers)
    df_games = pd.json_normalize(r.json(), sep='_')

    df_games['Day'] = pd.to_datetime(df_games['Day']).dt.date
    df_games = df_games.fillna(np.nan).replace([np.nan], [None])

    games_dict = df_games.to_dict(orient='records')
    for game in games_dict:
        FantasyDataGames.objects.update_or_create(**game)


# Football Outsiders
def load_fo_fplus_ratings(season: int = None):
    if not season:
        week = cfbd_current_week()
        season = week['season']
    s3 = boto3.client('s3')
    mapping_file = s3.get_object(Bucket='bet-caddie', Key=f'ncaaf/{season} COLLEGE FOOTBALL F+ RATINGS.csv')
    body = mapping_file['Body']
    csv_string = body.read().decode('utf-8')
    df_fplus = pd.read_csv(StringIO(csv_string), sep=',')

    df_fplus.columns = df_fplus.columns.str.replace('+', '_plus')
    df_fplus = df_fplus[['Team', 'F_plus', 'OF_plus', 'DF_plus', 'FEI', 'SP_plus']]
    fplus_dict = df_fplus.to_dict(orient='records')

    for ratings in fplus_dict:
        FootballOutsidersFPlusRatings.objects.update_or_create(**ratings)

# Odds API
