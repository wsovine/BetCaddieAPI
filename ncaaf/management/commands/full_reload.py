from django.core.management import BaseCommand
from django.conf import settings

from ncaaf.services import cfbd_games_api, cfbd_current_week
from ncaaf.tasks import load_fd_games, load_fd_teams, load_fo_fplus_ratings, load_mappings
from ncaaf.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        FantasyDataGames.objects.all().delete()
        FantasyDataLeagueHierarchy.objects.all().delete()

        load_fd_teams()

        # Load Previous Seasons
        backfill_seasons = settings.NCAAF_BACKFILL_SEASONS
        for season in backfill_seasons:
            weeks = cfbd_games_api.get_calendar(season)
            for week in weeks:
                FootballOutsidersFPlusRatings.objects.all().delete()
                load_fo_fplus_ratings(season=season, season_type=week.season_type, week=week.week)

                TeamMappings.objects.all().delete()
                load_mappings()

                post_season = False if week.season_type == 'regular' else True
                load_fd_games(season=season, post_season=post_season, week=week.week)

        # Load Current Season
        current_week = cfbd_current_week()
        weeks = cfbd_games_api.get_calendar(current_week['season'])
        for week in weeks:
            FootballOutsidersFPlusRatings.objects.all().delete()
            load_fo_fplus_ratings(
                season=week.season,
                season_type=week.season_type,
                week=week.week
            )

            TeamMappings.objects.all().delete()
            load_mappings()

            post_season = False if week.season_type == 'regular' else True
            load_fd_games(season=week.season, post_season=post_season, week=week.week)
