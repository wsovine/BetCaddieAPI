from datetime import datetime, timedelta

import cfbd
from dateutil import parser
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ncaaf.services import cfbd_bet_api, cfbd_current_week


# SEASONS AND WEEKS
@api_view(['GET'])
def current_or_latest_week(request) -> JsonResponse:
    return JsonResponse(cfbd_current_week())


# GAMES
@api_view(['GET'])
def game_list(request, season: int, season_type: str, week: int) -> JsonResponse:
    games = cfbd_bet_api.get_lines(year=season, season_type=season_type, week=week)
    return JsonResponse({'games': [g.to_dict() for g in games]})
