from django.test import TestCase
from django.test.utils import setup_test_environment
from cyclope.models import SiteSettings, StaticPage, MenuItem
from django.contrib.sites.models import Site
from cyclope.core import frontend
from django.conf import settings
from cyclope import settings as cyc_settings

def create_static_page():
    static_page = StaticPage(name='A page')
    static_page.save()


class ModelTestCase(TestCase):
    """Test that models can be created"""

    def setUp(self):
        site = Site(domain="mydomain.com", name="mydomain")
        site.save()

    def test_site_settings_creation(self):
        site = Site.objects.get(name='mydomain')
        theme = cyc_settings.CYCLOPE_THEMES.available[0]
        instance = SiteSettings(site=site,
                                theme=theme,
                                allow_comments='YES')
        instance.save()
        saved_instance = SiteSettings.objects.get(site=site)
        self.assertEqual(saved_instance.site, site)

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
