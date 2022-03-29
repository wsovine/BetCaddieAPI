from django.core.management import BaseCommand

from ncaaf.tasks import load_fd_games


class Command(BaseCommand):

    help = 'Load games from fantasy data / sport data api'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--season',
            '-S',
            action='store',
            help='Season to load games for (e.g. 2021)',
        )

        # Named (optional) arguments
        parser.add_argument(
            '--post_season',
            action='store_true',
            help='Load post season games for a given season',
        )

    def handle(self, *args, **options):
        post_season = options['post_season']
        load_fd_games(season=options['season'], post_season=post_season)
