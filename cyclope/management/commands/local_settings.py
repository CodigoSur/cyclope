from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.utils.translation import ugettext as _
import os.path
from django.conf import settings
import shutil
from django.utils.crypto import get_random_string
from optparse import make_option

class Command(BaseCommand):
    help = _('Copies settings.py file from local project template to current project')
    
    #NOTE django > 1.8 uses argparse instead of optparse module, 
    #so "You are encouraged to exclusively use **options for new commands."
    #https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/
    option_list = BaseCommand.option_list + (
        make_option('--project_name',
            action='store',
            dest='project_name',
            default='cyclope_project',
            help=_('Project folder name, as generated by cyclopeproject command')
        ),
    )
    
    def handle(self, *args, **options):
        # TODO(NumericA) Django > 1.8 includes BASE_DIR setting
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        CYCLOPE_DIR = os.path.join('/', * BASE_DIR.split('/')[:-3])
        TEMPLATE_PATH = os.path.join(CYCLOPE_DIR, 'cyclope/conf/project_template/settings.py')
        PROJECT_PATH = settings.CYCLOPE_PROJECT_PATH
        # COPY
        shutil.copy(TEMPLATE_PATH, PROJECT_PATH)
        # PARSE TEMPLATE VARS
        settings_file = os.path.join(PROJECT_PATH, 'settings.py')
        project_name = options['project_name']
        secret_key = self.get_random_secret_key()
        self.parse_settings_vars(settings_file, project_name, secret_key)
        
    def parse_settings_vars(self, settings_file, project_name, secret_key):
        f = open(settings_file, 'r')
        filedata = f.read()
        f.close()
        newdata = filedata.replace("{{ project_name }}", project_name)
        newdata = newdata.replace("{{ secret_key }}", secret_key)
        f = open(settings_file, 'w')
        f.write(newdata)
        f.close()
        
    def get_random_secret_key(self):
        # TODO(NumericA) Django > 1.8 from django.core.management.utils import get_random_secret_key
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        return get_random_string(50, chars)