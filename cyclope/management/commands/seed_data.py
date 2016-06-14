from django.core.management.base import BaseCommand, CommandError
from cyclope.models import Layout
from django.utils.translation import ugettext as _

class Command(BaseCommand):
    help = 'POPULATES LAYOUT SEED DATA'

    LYS = {
        'TRES COLUMNAS': {
            'name': _('TRES COLUMNAS'),
            'template': 'layout_three_columns.html',
            'image': 'layout_three_columns.png'
        },
        'DOS COLUMAS IZQUIERDA': {
            'name': _('DOS COLUMAS IZQUIERDA'),
            'template': 'layout_two_columns_left.html',
            'image': 'layout_two_columns_left.png'
        }, 
        'DOS COLUMNAS DERECHA': {
            'name': _('DOS COLUMNAS DERECHA'),
            'template': 'layout_two_columns_right.html',
            'image': 'layout_two_columns_right.png'
        },
        'MAGAZINE': {
            'name': _('MAGAZINE'),
            'template': 'layout_one_column.html',
            'image': 'layout_one_column.png'
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


    #TODO
    #def kill(self):
