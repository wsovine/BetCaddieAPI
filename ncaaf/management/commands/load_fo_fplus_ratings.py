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
            help='Season to load games for (e.g. 2021)',
        )

    def handle(self, *args, **options):
        load_fo_fplus_ratings(season=options['season'])
