from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from optparse import make_option
from django.utils.translation import ugettext as _

class Command(BaseCommand):
    help = 'Borrar un usuario por username'
   
     #NOTE django > 1.8 uses argparse instead of optparse module, 
     #so "You are encouraged to exclusively use **options for new commands."
     #https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/
    option_list = BaseCommand.option_list + (
        make_option('--username',
            action='store',
            dest='username',
            help=_('Username to delete')
        ),
    )

    def handle(self, *args, **options):
        username = options['username']
        if username:
            import pdb; pdb.set_trace()
            User.objects.filter(username=username).delete()
