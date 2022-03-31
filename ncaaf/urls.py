from django.urls import path
from ncaaf.views import *


urlpatterns = [
    path('current_or_latest_week/', current_or_latest_week, name='current_week'),
    path('games_list/<int:season>/<str:season_type>/<int:week>/', game_list, name='game_list'),
    path('weeks/<int:season>/', weeks_in_season, name='weeks')
]
