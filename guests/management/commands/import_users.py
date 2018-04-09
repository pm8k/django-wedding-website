from django.core.management import BaseCommand
from guests import create_users


class Command(BaseCommand):
    args = 'filename'
    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)
    def handle(self, filename, *args, **kwargs):
        print filename
        create_users.create_users(filename[0])
