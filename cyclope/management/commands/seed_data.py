from django.core.management.base import BaseCommand, CommandError
from cyclope.models import Layout
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from cyclope.models import Menu, MenuItem, Layout, SiteSettings, RegionView
from contact_form.models import ContactFormSettings
from django.contrib.auth.models import User, Group
from cyclope.apps.articles.models import Article
from cyclope.core.collections.models import Collection, Category, Categorization
from django.contrib.contenttypes.models import ContentType
from optparse import make_option

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
        },
        'NEWSLETTER': {
            'name': _('Newsletter'),
            'template': 'newsletter.html',
            'image': 'layout_newsletters.png'
        }
    }
    
    DEFAULT_VIEW_OPTIONS = '{"sort_by": "DATE-", "show_title": true, "show_description": true, "show_image": true, "items_per_page": 5, "limit_to_n_items": 0, "simplified": false, "traverse_children": false, "navigation": "TOP"}'

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
        # SITE
        site = self.create_site()
        # LAYOUTS
        self.create_layouts()
        ######
        # DEMO
        if options['demo']:           
            self.create_demo_objects(site)

    def create_site(self):
        # SITE
        if Site.objects.all():
            site = Site.objects.all()[0]
        else:
            site = Site()
            domain = "localhost:8000"
            #if kwargs.get('interactive', True):
            msg = "\nDomain name (leave empty for default: %s: " % domain
            input_domain = raw_input(msg)
            domain = input_domain or domain
            site_name = "CyclopeCMS demo"
            #if kwargs.get('interactive', True):
            msg = "\nSite name (leave empty for default: %s): " % site_name
            input_name = raw_input(msg)
            site_name = input_name or site_name
            #
            site.domain = domain
            site.name = site_name
            site.save()
        return site

    def create_layouts(self):
        for key, value in self.LYS.iteritems():
            layout = Layout()
            layout.name = value['name']
            layout.template = value['template']
            layout.image_path = value['image']
            layout.save()
        self.stdout.write(_("Layouts creados \n"))

    def create_demo_objects(self, site):
        # MAIN MENU
        menu = Menu(name="Main menu", main_menu=True)
        menu.save()
        #REGIONS
        default_layout = Layout.objects.get(slug='two-columns-right') # BLOG
        RegionView.objects.create(region='header', layout=default_layout, content_object=menu, weight=1, content_view='menuitems_hierarchy', view_options='{"align": "HORIZONTAL"}')
        site_content_type =ContentType.objects.get(name='site')
        RegionView.objects.create(region='right', layout=default_layout, content_type_id=site_content_type.pk, weight=1, content_view='search')
        # HOME (MENU ITEM)
        menu_item = MenuItem(menu=menu, name="Inicio", site_home=True, active=True, layout=default_layout)
        menu_item.save()
        # THEME
        site_settings = SiteSettings(site=site, theme="cyclope-bootstrap", default_layout=default_layout, allow_comments='YES')
        site_settings.save()
        # COLLECTION & CATEGORY
        collection = Collection.objects.create(name="Contenidos", description="Agrupa todos los contenidos generados en el sitio por el script de arranque.")#TODO, content_types=)
        category = collection.categories.create(name="Noticias")
        # ARTICLE (welcome)
        article = Article.objects.create(name="Te damos la bienvenida a CyclopeCMS", text="Morbi cursus, enim nec mollis condimentum, nisl nisl porta tortor, ut accumsan lorem metus et nunc. Aenean eget accumsan massa. In sodales ligula eu lectus efficitur tincidunt. Nunc non massa vulputate, pellentesque sapien ac, congue erat. Nam in quam lectus. Mauris hendrerit dignissim ex, in sollicitudin ipsum lacinia vitae. Aenean pellentesque diam quis quam mollis, ac mattis ante rutrum. Sed id vulputate ligula.")
        Categorization.objects.create(content_object=article, category=category)
        # Home
        menu_item.content_object = category
        menu_item.content_view = "contents" 
        menu_item.view_options = self.DEFAULT_VIEW_OPTIONS
        menu_item.save()
        # CONTACT FORM
        contact = ContactFormSettings(subject="Contact mail")
        contact.save()
        contact_menu_item = MenuItem(
            menu=menu, 
            name="Contacto", 
            layout=default_layout, 
            custom_url="/contact",
            content_object = contact,
            content_view = "contents",
            view_options = self.DEFAULT_VIEW_OPTIONS
        )
        contact_menu_item.save()
        # USER GROUPS
        for g in ("editors", "managers", "translators"):
            group, created = Group.objects.get_or_create(name=g)
            if created: #?
                group.save()
        #.
