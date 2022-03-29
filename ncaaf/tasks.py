import pandas as pd
from models import TeamMappings, FantasyDataLeagueHierarchy, FantasyDataGames
import requests

from services import fd_base_url, fd_headers, cfbd_current_week


# Mapping
def load_mappings():
    """
    Mapping table is manually created and saved in data/ncaaf_mappings.csv
    It links team ID's from different sources
    """
    df_mappings = pd.read_csv('data/ncaaf_mappings.csv', sep=',')
    mapping_dict = df_mappings.to_dict(orient='records')
    model_instances = [TeamMappings(**mapping) for mapping in mapping_dict]
    TeamMappings.objects.all().delete()
    TeamMappings.objects.bulk_create(model_instances)


# Fantasy Data .io
# fantasydata.io plan is restricted to 100 api calls per day, so makes
# sense to load the data into the database after the call.
def load_fd_teams():
    r = requests.get(f'{fd_base_url}LeagueHierarchy', headers=fd_headers)
    df_teams = pd.json_normalize(r.json(), sep='_')
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
    games_dict = df_games.to_dict(orient='records')
    model_instances = [FantasyDataGames(**game) for game in games_dict]
    for instance in model_instances:
        FantasyDataGames.objects.update_or_create(instance)


# Football Outsiders

# Odds API
