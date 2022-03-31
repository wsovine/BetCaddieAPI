from rest_framework import serializers

from ncaaf.models import FantasyDataGames, GameBetCalcs


class GameBetCalcsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameBetCalcs
        fields = "__all__"


class FantasyDataGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FantasyDataGames
        fields = "__all__"
