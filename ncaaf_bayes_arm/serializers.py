from rest_framework import serializers
from ncaaf_bayes_arm.models import BayesArm


class BayesArmSerializer(serializers.ModelSerializer):
    # datetime_aware = serializers.DateTimeField(source='datetime_aware')

    class Meta:
        model = BayesArm
        fields = '__all__'
