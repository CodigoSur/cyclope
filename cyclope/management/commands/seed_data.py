from django.core.management.base import BaseCommand, CommandError
from cyclope.models import Layout
from django.utils.translation import ugettext as _

class Command(BaseCommand):
    help = 'POPULATES LAYOUT SEED DATA'

    LYS = {
        'TRES COLUMNAS': {
            'name': _('Three columns'),
            'template': 'layout_three_columns.html',
            'image': 'layout_three_columns_thumbnail.png'
        },
        'DOS COLUMAS IZQUIERDA': {
            'name': _('Two columns Left'),
            'template': 'layout_two_columns_left.html',
            'image': 'layout_two_columns_left_thumbnail.png'
        }, 
        'DOS COLUMNAS DERECHA': {
            'name': _('Two columns Right'),
            'template': 'layout_two_columns_right.html',
            'image': 'layout_two_columns_right_thumbnail.png'
        },
        'MAGAZINE': {
            'name': _('One column'),
            'template': 'layout_one_column.html',
            'image': 'layout_one_column_thumbnail.png'
        }
    }

    def handle(self, *args, **options):
        for key, value in self.LYS.iteritems():
            layout = Layout()
            layout.name = value['name']
            layout.template = value['template']
            layout.image_path = value['image']
            layout.save()
        self.stdout.write("Layouts creados \n")

