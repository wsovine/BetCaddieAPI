from django.http import JsonResponse
from rest_framework.decorators import api_view
from ncaaf_bayes_arm.models import BayesArm, CurrentOdds
from ncaaf_bayes_arm.serializers import BayesArmSerializer, CurrentOddsSerializer


@api_view(['GET'])
def bae_game_list(request, season: int, season_type: str, week: int) -> JsonResponse:
    game_objs = BayesArm.objects.filter(
        season=season,
        seasontype=3 if season_type == 'postseason' else 1,
        week=week
    ).order_by('datetime')

    games = BayesArmSerializer(game_objs, many=True)

    return JsonResponse({'games': games.data})


@api_view(['GET'])
def current_odds(request, sd_game_id: int):
    current_odd_objs = CurrentOdds.objects.filter(
        sports_data_game_id=sd_game_id
    )

    away_odds = [o for o in current_odd_objs if o.team_cfbd_id == o.cfbd_away_team_id]
    home_odds = [o for o in current_odd_objs if o.team_cfbd_id == o.cfbd_home_team_id]

    books = {o.bookmakers_title for o in current_odd_objs}

    data_list = []
    for book in books:
        away = list(filter(lambda o: o.bookmakers_title == book, away_odds))[0]
        home = list(filter(lambda o: o.bookmakers_title == book, home_odds))[0]
        data = {
            'book': book,
            'away': away.price,
            'home': home.price
        }
        data_list.append(data)

    return JsonResponse({'current_odds': data_list})
