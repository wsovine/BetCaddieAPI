from django.core.management import BaseCommand

from ncaaf.tasks import load_mappings


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_mappings()