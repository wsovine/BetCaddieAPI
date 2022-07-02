from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from ncaaf_bayes_arm.models import BayesArm
from ncaaf_bayes_arm.serializers import BayesArmSerializer


@api_view(['GET'])
def bae_game_list(request, season: int, season_type: str, week: int) -> JsonResponse:
    game_objs = BayesArm.objects.filter(
        season=season,
        seasontype=3 if season_type == 'postseason' else 1,
        week=week
    ).order_by('datetime')

    print(game_objs)

    games = BayesArmSerializer(game_objs, many=True)

    return JsonResponse({'games': games.data})
