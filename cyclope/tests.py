# *-- coding:utf-8 --*

from django.test import TestCase
from django.test.utils import setup_test_environment

from django.contrib.sites.models import Site
from django.conf import settings

from cyclope.models import SiteSettings, StaticPage, Menu, MenuItem, Layout
from cyclope.core import frontend
from cyclope import settings as cyc_settings

def create_static_page():
    static_page = StaticPage(name='A page')
    static_page.save()

def export_fixture(apps, filename=None):
    """
    Return dumpdata from apps. If filename write dumpdata to file.
    """
    from django.core.management.commands.dumpdata import Command as Dumpdata
    cmd = Dumpdata()
    dump = cmd.handle(*apps)
    if filename:
        f = open(filename, "w")
        f.write(dump)
        f.close()
    else:
        return dump

class SiteSettingsTestCase(TestCase):
    def setUp(self):
        self.site = Site(domain="mydomain.com", name="mydomain")
        self.site.save()

    def test_create_site(self):
        theme = cyc_settings.CYCLOPE_THEMES.available[0]
        site_settings = SiteSettings(site=self.site,
                                theme=theme,
                                allow_comments='YES')
        site_settings.save()
        self.assertEqual(site_settings.site, self.site)


class SiteTestCase(TestCase):
    def testSimplestSite(self):
        """
        Test the simplest creation of a Cyclope-site.
        """
        site = Site(domain="mydomain.com", name="mydomain")
        site.save()

        menu = Menu(name="Main menu", main_menu=True)
        menu.save()

        layout = Layout(name="one sidebar", template='one_sidebar.html')
        layout.save()

        menu_item = MenuItem(menu=menu, name="home", site_home=True, active=True, layout=layout)
        menu_item.save()

        theme = cyc_settings.CYCLOPE_THEMES.available[0]
        site_settings = SiteSettings(site=site,
                                theme=theme,
                                default_layout=layout,
                                allow_comments='YES')



        site_settings.save()
        response = self.client.get("/")
        self.assertTemplateUsed(response, u'cyclope/themes/neutrona/one_sidebar.html')

        # FIXME: add some more usefull asserts

    def testBugWithoutLayout(self):
        site = Site(domain="mydomain.com", name="mydomain")
        site.save()
        menu = Menu(name="Main menu", main_menu=True)
        menu.save()
        menu_item = MenuItem(menu=menu, name="home", site_home=True, active=True)
        menu_item.save()

        theme = cyc_settings.CYCLOPE_THEMES.available[0]
        site_settings = SiteSettings(site=site,
                                theme=theme,
                                allow_comments='YES')
        site_settings.save()
        response = self.client.get("/")

    def testWithoutHomeMenuitem(self):
        site = Site(domain="mydomain.com", name="mydomain")
        site.save()
        theme = cyc_settings.CYCLOPE_THEMES.available[0]
        site_settings = SiteSettings(site=site,
                                theme=theme,
                                allow_comments='YES')

        site_settings.save()
        response = self.client.get("/")
        self.assertEqual(response.content,'La página de inicio no ha sido establecida.' )


class RegionTestCase(TestCase):
    fixtures = ['simplest_site.json']

    def setUp(self):
        pass

    def testAddRegion(self):
        raise NotImplementedError


class ModelTestCase(TestCase):
    """Test that models can be created"""

    def setUp(self):
        pass


    def test_site_settings_creation(self):
        pass

    def test_menu_creation(self):
        pass

    def test_menuitem_creation(self):
        pass

    def test_layout_creation(self):
        pass

    def test_regionview_creation(self):
        pass

    def test_staticpage_creation(self):
        instance = StaticPage(name='An instance')
        instance.save()
        an_instance = StaticPage.objects.get(slug='an-instance')
        self.assertEqual(an_instance.name, 'An instance')


class AutodiscoveredViewsTestCase(TestCase):
    urls = 'cyclope.test_urls'

    def test_autodiscovered_views(self):
#        setup_test_environment()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        for model in frontend.site._registry:
            for view in frontend.site._registry[model]:
                # we don't test region views here
                if not view.is_standard_view:
                    continue
                obj = model.objects.get(pk=1)
                response = self.client.get("/"+obj.get_instance_url(view.name))
                self.assertEqual(response.status_code, 200)


    #    # make sure the correct template was used
    #    self.assertTemplateUSed(response, 'myapp/myview.html')
    #    # make sure the template was passed the correct context
    #    self.assertEqual(response.context['foo'], 'bar')
