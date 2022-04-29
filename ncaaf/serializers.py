from rest_framework import serializers

from ncaaf.models import FantasyDataGames, CeloBetCalcs, FantasyDataLeagueHierarchy, ArmBetCalcs


class CeloBetCalcsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CeloBetCalcs
        fields = "__all__"


class FantasyDataTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = FantasyDataLeagueHierarchy
        fields = '__all__'


class FantasyDataGameSerializer(serializers.ModelSerializer):
    celobetcalcs = CeloBetCalcsSerializer(read_only=True)
    AwayTeam = FantasyDataTeamSerializer(read_only=True)
    HomeTeam = FantasyDataTeamSerializer(read_only=True)

    class Meta:
        model = FantasyDataGames
        fields = "__all__"


class ArmBetCalcsSerializer(serializers.ModelSerializer):
    cfbd_game_id = serializers.IntegerField()

    class Meta:
        model = ArmBetCalcs
        fields = "__all__"
