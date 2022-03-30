from rest_framework import serializers

from ncaaf.models import FantasyDataGames


class FantasyDataGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FantasyDataGames
        fields = "__all__"
