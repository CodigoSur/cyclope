from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.utils.translation import ugettext as _
import os.path
from django.conf import settings
import shutil

class Command(BaseCommand):
    help = _('Copies settings.py file from local project template to current project')
    
    def handle(self, *args, **options):
        # TODO(NumericA) Django > 1.8 includes BASE_DIR setting
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        CYCLOPE_DIR = os.path.join('/', * BASE_DIR.split('/')[:-3])
        TEMPLATE_DIR = CYCLOPE_DIR + '/cyclope/conf/project_template/settings.py'
        shutil.copy(TEMPLATE_DIR, settings.CYCLOPE_PROJECT_PATH)
        
