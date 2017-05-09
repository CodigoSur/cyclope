from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.utils.translation import ugettext as _

class Command(BaseCommand):
    help = _('Aplica las migraciones de Django para migrar la bd de un proyecto Cyclope a django 1.9')

    def handle(self, *args, **options):
        # python manage.py migrate --fake-initial auth 0004_alter_user_username_opts
        call_command('migrate', 'auth', '0004_alter_user_username_opts', interactive=False, fake_initial=True)
        # python manage.py migrate auth 0005_alter_user_last_login_null
        call_command('migrate', 'auth', '0005_alter_user_last_login_null', interactive=False)
        # python manage.py migrate --fake-initial contenttypes 0001_initial
        call_command('migrate', 'contenttypes', '0001_initial', interactive=False, fake_initial=True)
        # python manage.py migrate contenttypes 0002_remove_content_type_name
        call_command('migrate', 'contenttypes', '0002_remove_content_type_name', interactive=False)
        # python mange.py migrate --fake-initial
        call_command('migrate', interactive=False, fake_initial=True)
