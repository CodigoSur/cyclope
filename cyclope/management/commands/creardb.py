from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from optparse import make_option
from django.utils.translation import ugettext as _

class Command(BaseCommand):
    help = _('Creates initial CyclopeCMS DB.')
    
    #NOTE django > 1.8 uses argparse instead of optparse module, 
    #so "You are encouraged to exclusively use **options for new commands."
    #https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/
    option_list = BaseCommand.option_list + (
        make_option('--demo',
            action='store_true',
            dest='demo',
            default=False,
            help=_('Fill site with demo elements (Menus, Cateories, Article...)')
        ),
    )
   
    def handle(self, *args, **options):
        # python manage.py syncdb --noinput
        call_command('syncdb', interactive=False, migrate_all=True)
        # python manage.py migrate --fake
        call_command('migrate', fake=True)
        # python manage.py loaddata default_groups.json
        call_command('loaddata', 'default_groups.json')
        # python manage.py seed_data (--demo)
        call_command('seed_data', demo=options['demo'])
