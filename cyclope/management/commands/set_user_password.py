from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from optparse import make_option
from django.utils.translation import ugettext as _

class Command(BaseCommand):
    help = 'Cambiar el Password de un Usuario Cyclope'
   
     #NOTE django > 1.8 uses argparse instead of optparse module, 
     #so "You are encouraged to exclusively use **options for new commands."
     #https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/
    option_list = BaseCommand.option_list + (
        make_option('--username',
            action='store',
            dest='username',
            help=_('Username')
        ),
        make_option('--new-password',
            action='store',
            dest='new_password',
            help=_('New password')
        )
    )

    def handle(self, *args, **options):
        username = options['username']
        new_password = options['new_password']
        if not username:
            raise CommandError(_("Missing --username to change password"))
        if not new_password:
            raise CommandError(_("Missing --new_password to set"))
        #
        user = User.objects.filter(username=username)
        user.set_password(new_password)
        user.save()
