from datetime import datetime, timedelta

import cfbd
from dateutil import parser
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view

from ncaaf.models import FantasyDataGames
from ncaaf.serializers import FantasyDataGameSerializer
from ncaaf.services import cfbd_bet_api, cfbd_current_week, cfbd_games_api


# SEASONS AND WEEKS
@api_view(['GET'])
def current_or_latest_week(request) -> JsonResponse:
    return JsonResponse(cfbd_current_week())


# GAMES
@api_view(['GET'])
def game_list(request, season: int, season_type: str, week: int) -> JsonResponse:
    cfbd_games = cfbd_games_api.get_games(year=season, season_type=season_type, week=week)
    fd_games = FantasyDataGames.objects.filter(
        Season=season,
        SeasonType=3 if season_type == 'postseason' else 1,
        Week=week
    ).order_by('DateTime')

    games = FantasyDataGameSerializer(fd_games, many=True)

    return JsonResponse({'games': games.data})
