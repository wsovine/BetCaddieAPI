from django.urls import path
from ncaaf_bayes_arm.views import *


urlpatterns = [
    path('bae/games_list/<int:season>/<str:season_type>/<int:week>/', bae_game_list, name='game_list'),
    path('bae/odds/<int:sd_game_id>/', current_odds, name='odds'),
]
