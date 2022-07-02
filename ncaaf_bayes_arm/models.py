from django.db import models


class BayesArm(models.Model):
    gameid = models.BigIntegerField(primary_key=True)
    awayteam = models.TextField(blank=True, null=True)
    hometeam = models.TextField(blank=True, null=True)
    season = models.BigIntegerField(blank=True, null=True)
    seasontype = models.BigIntegerField(blank=True, null=True)
    week = models.BigIntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    awayteamname = models.TextField(blank=True, null=True)
    hometeamname = models.TextField(blank=True, null=True)
    awayteamscore = models.BigIntegerField(blank=True, null=True)
    hometeamscore = models.BigIntegerField(blank=True, null=True)
    away_odds = models.FloatField(blank=True, null=True)
    home_odds = models.FloatField(blank=True, null=True)
    away_sb_open = models.FloatField(blank=True, null=True)
    home_sb_open = models.FloatField(blank=True, null=True)
    away_sb_latest = models.FloatField(blank=True, null=True)
    home_sb_latest = models.FloatField(blank=True, null=True)
    away_prediction = models.FloatField(blank=True, null=True)
    home_prediction = models.FloatField(blank=True, null=True)
    away_hdi_lower = models.FloatField(blank=True, null=True)
    home_hdi_lower = models.FloatField(blank=True, null=True)
    away_hdi_upper = models.FloatField(blank=True, null=True)
    home_hdi_upper = models.FloatField(blank=True, null=True)
    prediction_std = models.FloatField(blank=True, null=True)
    away_er = models.FloatField(blank=True, null=True)
    home_er = models.FloatField(blank=True, null=True)
    away_upset_watch = models.BigIntegerField(blank=True, null=True)
    home_upset_watch = models.BigIntegerField(blank=True, null=True)
    away_color = models.TextField(blank=True, null=True)
    home_color = models.TextField(blank=True, null=True)
    away_alt_color = models.TextField(blank=True, null=True)
    home_alt_color = models.TextField(blank=True, null=True)
    away_logos = models.TextField(blank=True, null=True)
    home_logos = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'bayes_arm_view'

