from django.core.management import BaseCommand

from ncaaf.tasks import load_fd_teams


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_fd_teams()
