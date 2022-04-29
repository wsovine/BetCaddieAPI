from django.urls import path
from ncaaf.views import *


urlpatterns = [
    path('current_or_latest_week/', current_or_latest_week, name='current_week'),
    path('arm/games_list/<int:season>/<str:season_type>/<int:week>/', arm_game_list, name='game_list'),
    path('celo/games_list/<int:season>/<str:season_type>/<int:week>/', celo_game_list, name='game_list'),
    path('weeks/<int:season>/', weeks_in_season, name='weeks')
]
