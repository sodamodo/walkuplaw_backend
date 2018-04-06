import sys
from django.core.management.base import BaseCommand
from walkup_law.walkup_law.fixtures import create_fixtures

class Command(BaseCommand):

    def handle(self, *args, **options):
        sys.stdout.write('Create Fixtures\r\n')
        create_fixtures()
        sys.stdout.write('fixtures created' + '\r\n')
        sys.stdout.write('=====================================' + '\r\n')

