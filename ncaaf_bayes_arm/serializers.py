from rest_framework import serializers
from ncaaf_bayes_arm.models import BayesArm, CurrentOdds


class BayesArmSerializer(serializers.ModelSerializer):
    class Meta:
        model = BayesArm
        fields = '__all__'


class CurrentOddsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentOdds
        fields = '__all__'
