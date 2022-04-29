from django.http import JsonResponse
from rest_framework.decorators import api_view

from ncaaf.models import FantasyDataGames, ArmBetCalcs
from ncaaf.serializers import FantasyDataGameSerializer, ArmBetCalcsSerializer
from ncaaf.services import cfbd_current_week, cfbd_games_api


# SEASONS AND WEEKS
@api_view(['GET'])
def current_or_latest_week(request) -> JsonResponse:
    return JsonResponse(cfbd_current_week())


@api_view(['GET'])
def weeks_in_season(request, season: int) -> JsonResponse:
    weeks = cfbd_games_api.get_calendar(season)
    return JsonResponse({'weeks': [week.to_dict() for week in weeks]})


# GAMES
@api_view(['GET'])
def celo_game_list(request, season: int, season_type: str, week: int) -> JsonResponse:
    fd_games = FantasyDataGames.objects.filter(
        Season=season,
        SeasonType=3 if season_type == 'postseason' else 1,
        Week=week
    ).order_by('DateTime')

    games = FantasyDataGameSerializer(fd_games, many=True)

    return JsonResponse({'games': games.data})


@api_view(['GET'])
def arm_game_list(request, season: int, season_type: str, week: int) -> JsonResponse:
    cfbd_games = cfbd_games_api.get_games(
        year=season,
        season_type=season_type,
        week=week
    )

    games = [g.to_dict() for g in cfbd_games]

    for game in games:
        try:
            armbetcalcs = ArmBetCalcs.objects.get(cfbd_game_id=game['id'])
        except ArmBetCalcs.DoesNotExist:
            armbetcalcs = ArmBetCalcs()

        game['armbetcalcs'] = ArmBetCalcsSerializer(armbetcalcs, many=False).data

    return JsonResponse({'games': games})
