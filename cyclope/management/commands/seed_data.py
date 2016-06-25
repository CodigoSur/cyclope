from django.core.management.base import BaseCommand, CommandError
from cyclope.models import Layout
from django.utils.translation import ugettext as _ # TODO NO TRADUCE
from django.contrib.sites.models import Site
from cyclope.models import Menu, MenuItem, Layout, SiteSettings
from contact_form.models import ContactFormSettings
from django.contrib.auth.models import User, Group

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
        # TODO clean_all()
        self.create_site()
        self.create_contact_form_settings()
        self.create_user_groups()

    def create_site(self):
        # SITE
        # Domain name
        domain = "localhost:8000"
        #if kwargs.get('interactive', True):
        msg = "\nDomain name (leave empty for default: %s: " % domain
        input_domain = raw_input(msg)
        domain = input_domain or domain
        # Site name
        site_name = "CyclopeCMS demo"
        #if kwargs.get('interactive', True):
        msg = "\nSite name (leave empty for default: %s): " % site_name
        input_name = raw_input(msg)
        site_name = input_name or site_name
        if Site.objects.all():
            site = Site.objects.all()[0]
        else:
            site = Site()
        site.domain = domain
        site.name = site_name
        site.save()
        # MAIN MENU
        menu = Menu(name="Main menu", main_menu=True)
        menu.save()
        # LAYOUTS
        self.create_layouts()###TODO in handle
        default_layout = Layout.objects.get(slug='two-columns-right') # BLOG
        # HOME (MENU ITEM)
        menu_item = MenuItem(menu=menu, name="home", site_home=True, active=True, layout=default_layout)
        menu_item.save()
        # THEME
        site_settings = SiteSettings(site=site, theme="cyclope-bootstrap", default_layout=default_layout, allow_comments='YES')
        site_settings.save()
        #.

    def create_layouts(self):
        for key, value in self.LYS.iteritems():
            layout = Layout()
            layout.name = value['name']
            layout.template = value['template']
            layout.image_path = value['image']
            layout.save()
        #self.stdout.write("Layouts creados \n")

    def create_contact_form_settings(self):
        cfs = ContactFormSettings(subject="Contact mail")
        cfs.save()

    def create_user_groups(self):
        for g in ("editors", "managers", "translators"):
            group, created = Group.objects.get_or_create(name=g)
            if created: #?
                group.save()

