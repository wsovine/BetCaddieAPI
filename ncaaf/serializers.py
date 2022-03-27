from abc import ABC

from rest_framework import serializers


class CFBDWeekSerializer(serializers.Serializer):
    first_game_start = serializers.DateTimeField()
    last_game_start = serializers.DateTimeField()
    season = serializers.IntegerField()
    season_type = serializers.CharField(max_length=120)
    week = serializers.IntegerField()
