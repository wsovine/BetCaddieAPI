# Generated by Django 3.2.5 on 2022-03-29 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FantasyDataLeagueHierarchy',
            fields=[
                ('TeamID', models.IntegerField(primary_key=True, serialize=False)),
                ('Key', models.CharField(max_length=120)),
                ('Active', models.BooleanField()),
                ('School', models.CharField(max_length=120)),
                ('Name', models.CharField(max_length=120)),
                ('StadiumID', models.IntegerField()),
                ('ApRank', models.IntegerField()),
                ('Wins', models.IntegerField()),
                ('Losses', models.IntegerField()),
                ('ConferenceWins', models.IntegerField()),
                ('ConferenceLosses', models.IntegerField()),
                ('TeamLogoUrl', models.URLField()),
                ('ConferenceID', models.IntegerField()),
                ('Conference', models.CharField(max_length=120)),
                ('ShortDisplayName', models.CharField(max_length=120)),
                ('RankWeek', models.IntegerField()),
                ('RankSeason', models.IntegerField()),
                ('RankSeasonType', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TeamMappings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fd_team_id', models.IntegerField()),
                ('fd_team_key', models.CharField(max_length=120)),
                ('fo_team', models.CharField(max_length=120)),
                ('cfbd_team_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FantasyDataGames',
            fields=[
                ('GameID', models.IntegerField(primary_key=True, serialize=False)),
                ('Season', models.IntegerField()),
                ('SeasonType', models.IntegerField()),
                ('Week', models.IntegerField()),
                ('Status', models.CharField(max_length=120)),
                ('Day', models.DateField()),
                ('DateTime', models.DateTimeField()),
                ('AwayTeam', models.CharField(max_length=120)),
                ('HomeTeam', models.CharField(max_length=120)),
                ('AwayTeamName', models.CharField(max_length=120)),
                ('HomeTeamName', models.CharField(max_length=120)),
                ('AwayTeamScore', models.IntegerField()),
                ('HomeTeamScore', models.IntegerField()),
                ('PointSpread', models.IntegerField()),
                ('OverUnder', models.IntegerField()),
                ('AwayTeamMoneyLine', models.IntegerField()),
                ('HomeTeamMoneyLine', models.IntegerField()),
                ('StadiumID', models.IntegerField()),
                ('Title', models.CharField(max_length=120)),
                ('HomeRotationNumber', models.BigIntegerField()),
                ('AwayRotationNumber', models.BigIntegerField()),
                ('NeutralVenue', models.BooleanField()),
                ('AwayPointSpreadPayout', models.IntegerField()),
                ('HomePointSpreadPayout', models.IntegerField()),
                ('OverPayout', models.IntegerField()),
                ('UnderPayout', models.IntegerField()),
                ('Periods', models.JSONField()),
                ('Stadium_StadiumID', models.IntegerField()),
                ('Stadium_Active', models.BooleanField()),
                ('Stadium_Name', models.CharField(max_length=120)),
                ('Stadium_Dome', models.BooleanField()),
                ('Stadium_City', models.CharField(max_length=120)),
                ('Stadium_State', models.CharField(max_length=2)),
                ('Stadium_GeoLat', models.FloatField()),
                ('Stadium_GeoLong', models.FloatField()),
                ('AwayTeamID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='away_team', to='ncaaf.fantasydataleaguehierarchy')),
                ('HomeTeamID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='home_team', to='ncaaf.fantasydataleaguehierarchy')),
            ],
        ),
    ]
