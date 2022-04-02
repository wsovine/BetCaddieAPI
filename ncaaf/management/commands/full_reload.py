from django.core.management import BaseCommand
from django.conf import settings

from ncaaf.tasks import load_fd_games, load_fd_teams, load_fo_fplus_ratings, load_mappings
from ncaaf.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        FantasyDataGames.objects.all().delete()
        FantasyDataLeagueHierarchy.objects.all().delete()

        backfill_seasons = settings.NCAAF_BACKFILL_SEASONS

        load_fd_teams()
        for season in backfill_seasons:
            FootballOutsidersFPlusRatings.objects.all().delete()
            load_fo_fplus_ratings(season=season)

            TeamMappings.objects.all().delete()
            load_mappings()

            load_fd_games(season=season, post_season=False)
            load_fd_games(season=season, post_season=True)
