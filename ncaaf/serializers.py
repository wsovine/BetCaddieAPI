from rest_framework import serializers

from ncaaf.models import FantasyDataGames, GameBetCalcs, FantasyDataLeagueHierarchy


class GameBetCalcsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameBetCalcs
        fields = "__all__"


class FantasyDataTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = FantasyDataLeagueHierarchy
        fields = '__all__'


class FantasyDataGameSerializer(serializers.ModelSerializer):
    gamebetcalcs = GameBetCalcsSerializer(read_only=True)
    AwayTeam = FantasyDataTeamSerializer(read_only=True)
    HomeTeam = FantasyDataTeamSerializer(read_only=True)

    class Meta:
        model = FantasyDataGames
        fields = "__all__"
