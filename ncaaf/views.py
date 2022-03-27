from datetime import datetime, timedelta

import cfbd
from dateutil import parser
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ncaaf.services import cfbd_games_api, cfbd_bet_api


# SEASONS AND WEEKS
@api_view(['GET'])
def current_or_latest_week(request) -> JsonResponse:
    today = datetime.now()
    cur_year = today.year

    cal = cfbd_games_api.get_calendar(cur_year)
    while len(cal) <= 0:
        cur_year -= 1
        cal = cfbd_games_api.get_calendar(cur_year)

    cur_week = cfbd.Week()
    if today.date() > parser.isoparse(cal[-1].last_game_start).date():
        cur_week = cal[-1]
    else:
        for week in cal:
            start = parser.isoparse(week.first_game_start)
            end = parser.isoparse(week.last_game_start) + timedelta(hours=4)
            if today in (start, end):
                cur_week = week

    return JsonResponse(cur_week.to_dict())


# GAMES
@api_view(['GET'])
def game_list(request, season: int, season_type: str, week: int) -> JsonResponse:
    games_cfbd = cfbd_games_api.get_games(year=season, season_type=season_type, week=week)

    response = []
    for game in games_cfbd:
        game_data = {
            'id': game.id,
            'away_team': game.away_team,
            'away_id': game.away_id,
            'away_points': game.away_points,
            'home_team': game.home_team,
            'home_id': game.home_id,
            'home_points': game.home_points,
            'date_str': parser.isoparse(game.start_date).strftime('%c'),
            'neutral_site': game.neutral_site
            }
        response.append(game_data)

    return JsonResponse({'games': response})
