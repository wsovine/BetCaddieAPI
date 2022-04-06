from django.core.management import BaseCommand

from ncaaf.tasks import load_fo_fplus_ratings


class Command(BaseCommand):

    help = 'Load Football Outsiders F+ tables from S3 bucket'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--season',
            '-S',
            action='store',
            help='Season to load ratings for (e.g. 2021)',
        )

        parser.add_argument(
            '--season_type',
            '-T',
            action='store',
            help='Season type to load ratings for (e.g. regular)',
        )

        parser.add_argument(
            '--week',
            '-W',
            action='store',
            help='Week to load ratings for (e.g. 7)',
        )

    def handle(self, *args, **options):
        load_fo_fplus_ratings(
            season=options['season'],
            season_type=options['season_type'],
            week=options['week']
        )
