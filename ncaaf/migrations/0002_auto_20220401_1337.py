# Generated by Django 3.2.5 on 2022-04-01 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ncaaf', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gamebetcalcs',
            old_name='away_ml_bayes_er',
            new_name='away_ml_diff',
        ),
        migrations.RenameField(
            model_name='gamebetcalcs',
            old_name='home_ml_bayes_er',
            new_name='home_ml_diff',
        ),
        migrations.AddField(
            model_name='gamebetcalcs',
            name='away_ml_prob_less_vig',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='gamebetcalcs',
            name='home_ml_prob_less_vig',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='gamebetcalcs',
            name='ml_overround',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='gamebetcalcs',
            name='ml_vig',
            field=models.FloatField(null=True),
        ),
    ]
