from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Creates initial CyclopeCMS DB.'
    
    def handle(self, *args, **options):
        # python manage.py syncdb --noinput
        call_command('syncdb', interactive=False, migrate_all=True)
        # python manage.py migrate --fake
        call_command('migrate', fake=True)
        # python manage.py loaddata default_groups.json
        call_command('loaddata', 'default_groups.json')
        # python manage.py seed_data --demo
        call_command('seed_data', demo=True)
