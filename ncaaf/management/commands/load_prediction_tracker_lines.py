from django.core.management import BaseCommand

from ncaaf.models import ArmBetCalcs
from ncaaf.tasks import load_prediction_tracker_lines


class Command(BaseCommand):

    help = 'Load Prediction Tracker Lines from S3 bucket'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--season',
            '-S',
            action='store',
            help='Season to load lines for (e.g. 2021)',
        )

        parser.add_argument(
            '--season_type',
            '-T',
            action='store',
            help='Season type to load lines for (e.g. regular)',
        )

        parser.add_argument(
            '--week',
            '-W',
            action='store',
            help='Week to load lines for (e.g. 7)',
        )

    def handle(self, *args, **options):
        load_prediction_tracker_lines(
            season=options['season'],
            season_type=options['season_type'],
            week=options['week']
        )
