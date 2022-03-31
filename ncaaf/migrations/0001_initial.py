# Generated by Django 3.2.5 on 2022-03-31 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FantasyDataGames',
            fields=[
                ('GameID', models.IntegerField(primary_key=True, serialize=False)),
                ('Season', models.IntegerField(blank=True, null=True)),
                ('SeasonType', models.IntegerField(blank=True, null=True)),
                ('Week', models.IntegerField(blank=True, null=True)),
                ('Status', models.CharField(blank=True, max_length=120, null=True)),
                ('Day', models.DateField(blank=True, null=True)),
                ('DateTime', models.DateTimeField(blank=True, null=True)),
                ('AwayTeamName', models.CharField(blank=True, max_length=120, null=True)),
                ('HomeTeamName', models.CharField(blank=True, max_length=120, null=True)),
                ('AwayTeamScore', models.IntegerField(blank=True, null=True)),
                ('HomeTeamScore', models.IntegerField(blank=True, null=True)),
                ('PointSpread', models.IntegerField(blank=True, null=True)),
                ('OverUnder', models.IntegerField(blank=True, null=True)),
                ('AwayTeamMoneyLine', models.IntegerField(blank=True, null=True)),
                ('HomeTeamMoneyLine', models.IntegerField(blank=True, null=True)),
                ('StadiumID', models.IntegerField(blank=True, null=True)),
                ('Title', models.CharField(blank=True, max_length=120, null=True)),
                ('HomeRotationNumber', models.BigIntegerField(blank=True, null=True)),
                ('AwayRotationNumber', models.BigIntegerField(blank=True, null=True)),
                ('NeutralVenue', models.BooleanField(blank=True, null=True)),
                ('AwayPointSpreadPayout', models.IntegerField(blank=True, null=True)),
                ('HomePointSpreadPayout', models.IntegerField(blank=True, null=True)),
                ('OverPayout', models.IntegerField(blank=True, null=True)),
                ('UnderPayout', models.IntegerField(blank=True, null=True)),
                ('Periods', models.JSONField(blank=True, null=True)),
                ('Stadium_StadiumID', models.IntegerField(blank=True, null=True)),
                ('Stadium_Active', models.BooleanField(blank=True, null=True)),
                ('Stadium_Name', models.CharField(max_length=120)),
                ('Stadium_Dome', models.BooleanField(blank=True, null=True)),
                ('Stadium_City', models.CharField(blank=True, max_length=120, null=True)),
                ('Stadium_State', models.CharField(blank=True, max_length=2, null=True)),
                ('Stadium_GeoLat', models.FloatField(blank=True, null=True)),
                ('Stadium_GeoLong', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FantasyDataLeagueHierarchy',
            fields=[
                ('TeamID', models.IntegerField(primary_key=True, serialize=False)),
                ('Key', models.CharField(blank=True, max_length=120, null=True)),
                ('Active', models.BooleanField(blank=True, null=True)),
                ('School', models.CharField(blank=True, max_length=120, null=True)),
                ('Name', models.CharField(blank=True, max_length=120, null=True)),
                ('StadiumID', models.IntegerField(blank=True, null=True)),
                ('ApRank', models.IntegerField(blank=True, null=True)),
                ('Wins', models.IntegerField(blank=True, null=True)),
                ('Losses', models.IntegerField(blank=True, null=True)),
                ('ConferenceWins', models.IntegerField(blank=True, null=True)),
                ('ConferenceLosses', models.IntegerField(blank=True, null=True)),
                ('TeamLogoUrl', models.URLField(blank=True, null=True)),
                ('ConferenceID', models.IntegerField(blank=True, null=True)),
                ('Conference', models.CharField(blank=True, max_length=120, null=True)),
                ('ShortDisplayName', models.CharField(blank=True, max_length=120, null=True)),
                ('RankWeek', models.IntegerField(blank=True, null=True)),
                ('RankSeason', models.IntegerField(blank=True, null=True)),
                ('RankSeasonType', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FootballOutsidersFPlusRatings',
            fields=[
                ('Team', models.CharField(max_length=120, primary_key=True, serialize=False)),
                ('F_plus', models.FloatField()),
                ('OF_plus', models.FloatField()),
                ('DF_plus', models.FloatField()),
                ('FEI', models.FloatField()),
                ('SP_plus', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='GameBetCalcs',
            fields=[
                ('fd_game', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='ncaaf.fantasydatagames')),
                ('away_elo_pre', models.IntegerField(null=True)),
                ('home_elo_pre', models.IntegerField(null=True)),
                ('away_elo_prob', models.FloatField(null=True)),
                ('home_elo_prob', models.FloatField(null=True)),
                ('away_elo_post', models.IntegerField(null=True)),
                ('home_elo_post', models.IntegerField(null=True)),
                ('home_hfa_elo_adj', models.IntegerField(null=True)),
                ('away_elo_adj', models.IntegerField(null=True)),
                ('home_elo_adj', models.IntegerField(null=True)),
                ('away_scoring_matchup', models.FloatField(null=True)),
                ('home_scoring_matchup', models.FloatField(null=True)),
                ('away_matchup_elo_adj', models.IntegerField(null=True)),
                ('home_matchup_elo_adj', models.IntegerField(null=True)),
                ('away_ml_implied_prob', models.FloatField(null=True)),
                ('home_ml_implied_prob', models.FloatField(null=True)),
                ('away_ml_bayes_prob', models.FloatField(null=True)),
                ('home_ml_bayes_prob', models.FloatField(null=True)),
                ('away_ml_er', models.FloatField(null=True)),
                ('home_ml_er', models.FloatField(null=True)),
                ('away_ml_bayes_er', models.FloatField(null=True)),
                ('home_ml_bayes_er', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeamMappings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cfbd_team_id', models.IntegerField(blank=True, null=True)),
                ('fd_team', models.ForeignKey(blank=True, db_column='fd_team', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='fd_team', to='ncaaf.fantasydataleaguehierarchy')),
                ('fo_team', models.ForeignKey(blank=True, db_column='fo_team', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ncaaf.footballoutsidersfplusratings')),
            ],
        ),
        migrations.CreateModel(
            name='TeamCalculatedRatings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elo', models.IntegerField()),
                ('mapping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ncaaf.teammappings')),
            ],
        ),
        migrations.AddField(
            model_name='fantasydatagames',
            name='AwayTeam',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='away_team', to='ncaaf.fantasydataleaguehierarchy'),
        ),
        migrations.AddField(
            model_name='fantasydatagames',
            name='HomeTeam',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='home_team', to='ncaaf.fantasydataleaguehierarchy'),
        ),
    ]
