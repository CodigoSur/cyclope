#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Código Sur - Nuestra América Asoc. Civil / Fundación Pacificar.
# All rights reserved.
#
# This file is part of Cyclope.
#
# Cyclope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cyclope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django import forms
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template import TemplateSyntaxError, Template, Context
from django import template
from django.db.models import get_model

from cyclope.models import SiteSettings, Menu, MenuItem
from cyclope.models import Layout, RegionView, Author
from cyclope.core import frontend
from cyclope.core.collections.models import *
from cyclope.templatetags.cyclope_utils import do_join
from cyclope.apps.staticpages.models import StaticPage
from cyclope.apps.articles.models import Article
from cyclope.apps.medialibrary.models import *
from cyclope.apps.polls.models import *
from cyclope.apps.forum.models import *
from cyclope.apps.feeds.models import Feed
from cyclope.fields import MultipleField
from cyclope.sitemaps import CollectionSitemap, CategorySitemap, MenuSitemap
from cyclope.forms import SiteSettingsAdminForm, LayoutAdminForm
from cyclope import themes


def create_static_page(name=None):
    if name is None:
        name = 'A page'
    return StaticPage.objects.create(name=name)

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

def get_instance_url(model_instance, view_name):
    #TODO(nicoechaniz): this seems like a bad name. it returns the URL for an instance and for a non-instance as well. Also this code is repeated in many model files.
    view = cyclope.core.frontend.site.get_view(model_instance.__class__, view_name)

    if view.is_default:
        return '%s/%s/'\
                % (model_instance._meta.object_name.lower(),
                   model_instance.slug)

    if view.is_instance_view:
        return '%s/%s/View/%s'\
                % (model_instance._meta.object_name.lower(),
                   model_instance.slug, view_name)
    else:
        return '%s/View/%s'\
                % (model_instance._meta.object_name.lower(), view_name)


def get_content_urls(test_object):
    content_urls = []
    for view in frontend.site._registry[test_object.__class__]:
        if view.is_content_view:
            content_urls.append('/'+ get_instance_url(test_object, view.name))
    return content_urls


def get_region_views(test_model):
    return [ view for view in frontend.site._registry[test_model]
             if view.is_region_view ]

def add_region_view(model, view_name, content_object=None):
    layout = get_default_layout()
    content_type = ContentType.objects.get(model=model._meta.module_name)
    content_view = view_name
    region = 'after_fire'
    region_view = RegionView(layout=layout, content_type=content_type,
                             content_view=content_view, region=region,
                             content_object=content_object)
    region_view = region_view.save()
    return region_view


def get_default_site():
    if get_default_site.cache is None:
       get_default_site.cache = Site.objects.get_current()
    return get_default_site.cache

get_default_site.cache = None

def get_default_layout():
    if get_default_layout.cache is None:
       get_default_layout.cache = Layout.objects.all()[0]
    return get_default_layout.cache

get_default_layout.cache = None


class ViewableTestCase(TestCase):
    # this is an "abstract" test case which should be inherited but not run

#TODO (nicoechaniz): check how this base test class should be created to keep it out uf the test run

    fixtures = ['simplest_site.json']

    def setUp(self):
        if hasattr(self, 'test_model') and not hasattr(self, 'test_object'):
            self.test_object = self.test_model.objects.create(name='An instance')
        frontend.autodiscover()

    def test_creation(self):
        if hasattr(self, 'test_model'):
            an_instance = self.test_model.objects.get(slug='an-instance')
            self.assertEqual(an_instance.name, 'An instance')

    def test_content_views(self):
        if hasattr(self, 'test_object'):
            content_urls = get_content_urls(self.test_object)
            for url in content_urls:
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_region_views(self):
        if hasattr(self, 'test_model'):
            model_region_views = get_region_views(self.test_model)
            for view in model_region_views:
                content_object = None
                if view.is_region_view:
                    content_object = self.test_object
                add_region_view(self.test_model, view.name, content_object)
                response = self.client.get("/")
                self.assertContains(response,
                                    'class="regionview %s %s"' %
                                    (self.test_model._meta.module_name, view.name),
                                    count=1)


class SiteSettingsTestCase(TestCase):
    def setUp(self):
        self.site = Site(domain="mydomain.com", name="mydomain")
        self.site.save()

    def test_creation(self):
        site_settings = SiteSettings(site=self.site,
                                theme="neutrona",
                                allow_comments='YES')
        site_settings.save()
        self.assertEqual(site_settings.site, self.site)


class SiteTestCase(TestCase):
    def testSimplestSite(self):
        """
        Test the simplest creation of a Cyclope-site.
        """
        # Simplest site should be created by syncdb
        response = self.client.get("/")
        self.assertTemplateUsed(response,
                                u'cyclope/themes/neutrona/main.html')

    def testBugMenuItemWithoutLayout(self):
        # saving a MenuItem without setting a default site Layout failed
        site = get_default_site()
        menu = Menu.objects.get(main_menu=True)
        menu_item = MenuItem(menu=menu, name="without_layout", active=True)
        menu_item.save()

        site_settings = SiteSettings.objects.get(site=site)
        site_settings.save()
        response = self.client.get("/")


    def testSiteWithoutDefaultLayout(self):
        site = get_default_site()
        site_settings = SiteSettings.objects.get(site=site)
        site_settings.default_layout = None
        site_settings.save()
        response = self.client.get("/")
        self.assertEqual(response.content, 'You need to select a layout for the site')
        site_settings.default_layout = get_default_layout()
        site_settings.save()
        response = self.client.get("/")
        self.assertNotEqual(response.content, 'You need to select a layout for the site')
        #TODO(nicoechaniz): testing for the response content is weak; look for a better option
        # this view should use a standard error template and we should check that the template was used and some message id


    def testSiteWithoutHomeMenuitem(self):
        home = MenuItem.objects.get(site_home=True)
        home.site_home = False
        home.save()
        response = self.client.get("/")
        self.assertEqual(response.content, 'The site home page has not been set.')
        home.site_home = True
        home.save()
        response = self.client.get("/")
        self.assertNotEqual(response.content, 'The site home page has not been set.')
        #TODO(nicoechaniz): testing for the response content is weak; look for a better option


class RegressionTests(TestCase):

    def setUp(self):
        site = Site(domain="mydomain.com", name="mydomain")
        site.save()
        menu = Menu.objects.create(name="Main menu", main_menu=True)
        menu_item = MenuItem(menu=menu, name="home",
                                            site_home=True, active=True)
        menu_item.save()
        layout = Layout(name="default", template='main.html')
        layout.save()
        site_settings = SiteSettings.objects.create(site=site,
                                theme="neutrona",
                                allow_comments='YES')
        site_settings.default_layout = layout
        site_settings.save()


class RegionViewTestCase(TestCase):
    fixtures = ['simplest_site.json']

    def setUp(self):
        pass

    def testAddLayoutRegionView(self):
        layout = get_default_layout()
        content_type = ContentType.objects.get(model='staticpage')
        content_view = 'list'
        region = 'after_fire'
        region_view = RegionView(layout=layout, content_type=content_type,
                                 content_view=content_view, region=region)
        region_view.save()
        response = self.client.get("/")
        self.assertContains(response, 'class="regionview staticpage list"', count=1)

    def testAddLayoutRegionViewInstanceViewWithoutContent(self):
        """If the view in a region needs a content object and none is provided
        a template error will be raised when visiting a page using this layout."""
        #TODO(nicoechaniz): this is prevented at admin form level, but should also be checked at data level. See note in forms.py RegionViewInlineForm.clean() method
        layout = get_default_layout()
        content_type = ContentType.objects.get(model='staticpage')
        content_view = 'detail'
        region = 'after_fire'
        region_view = RegionView(layout=layout, content_type=content_type,
                                 content_view=content_view, region=region)
        region_view.save()
        self.assertRaises(TemplateSyntaxError, self.client.get, "/")


    def testAddLayoutRegionViewInstanceView(self):
        layout = get_default_layout()
        region_view = RegionView(layout=layout)
        content_type = ContentType.objects.get(model='staticpage')

        content_view = 'detail'
        static_page = create_static_page(
            name='test add layout region view instance view')
        object_id = static_page.id
        region = 'after_fire'
        region_view = RegionView(
            layout=layout, content_type=content_type, content_view=content_view,
            object_id=object_id, region=region)
        region_view.save()
        response = self.client.get("/")
        self.assertContains(response, 'class="regionview staticpage detail',
                            count=1)

    def tearDown(self):
        pass


class TemplateTagsTestCase(TestCase):
    def setUp(self):
        register = template.Library()
        register.tag(name='join', compile_function=do_join)

    def test_join_strings(self):
        t = Template("{% load cyclope_utils %}"
                     "{% join 'Cy' 'clo' 'pe' as variable %}"
                     "{{ variable }}")
        c = Context({})
        response = t.render(c)
        self.assertEqual(response, "Cyclope")


class SiteMapViewTestCase(TestCase):
    fixtures = ['simplest_site.json']
    test_model = Site

    def test_creation(self):
        site = Site.objects.create(name='An instance')
        an_instance = Site.objects.get(name='An instance')
        self.assertEqual(an_instance.name, 'An instance')

    def test_site_map_view(self):
        site = Site.objects.create(name='site', domain='site')
        col = Collection.objects.create(name='A collection')
        cat = Category(name='An instance', collection=col)
        cat.save()
        menu = Menu.objects.create(name='menu')
        content_type = ContentType.objects.get(model='site')
        MenuItem(name='site map', menu=menu,
                 content_type=content_type, content_view="map").save()
        res = self.client.get('/site-map')
        self.assertEqual(res.status_code, 200)


class StaticPageTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = StaticPage


class ArticleTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = Article

    def setUp(self):
        author = Author.objects.create(name="the author")
        self.test_object = Article.objects.create(name='An instance', author=author)
        frontend.autodiscover()


class DocumentTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = Document


class ExternalContentTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = ExternalContent


class FlashMovieTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = FlashMovie

    def setUp(self):
        self.test_object = FlashMovie.objects.create(name='An instance', flash="/")
        frontend.autodiscover()


class MovieClipTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = MovieClip


class PictureTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = Picture


class SoundTrackTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = SoundTrack


class PollTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = Poll


class CategoryTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = Category

    def setUp(self):
        # we need an authenticated user for some category views
        User = get_model('auth', 'user')
        self.user = User(username='admin')
        self.user.set_password('password')
        self.user.save()
        col = Collection.objects.create(name='A collection')
        self.test_object = Category(name='An instance', collection=col)
        self.test_object.save()
        frontend.autodiscover()


    def test_content_views(self):
        content_urls = get_content_urls(self.test_object)
        self.client.login(username='admin', password='password')
        for url in content_urls:
            self.assertEqual(self.client.get(url).status_code, 200)


class MoveCategoryTestCase(TestCase):
    def setUp(self):
        staticpage_ct = ContentType.objects.get(model="staticpage")
        collection_A = Collection.objects.create(name='collection A')
        collection_A.content_types.add(ContentType.objects.get(model="article"))
        collection_A.content_types.add(staticpage_ct)
        collection_A.save()

        collection_B = Collection.objects.create(name='collection B')
        collection_B.content_types.add(ContentType.objects.get(name="article"))
        collection_B.save()

        category = Category(name='Parent', collection=collection_A)
        category.save()

        child_category = Category(name='child', parent=category, collection=collection_A)
        child_category.save()

        children_of_child_category = Category(name='child child',
                                              parent=child_category,
                                              collection=collection_A)
        children_of_child_category.save()

        static_page = StaticPage.objects.create(name="static", text="prueba")
        static_page.categories.create(category=child_category)

        self.collection_A, self.collection_B = collection_A, collection_B
        self.category, self.child_category  = category, child_category
        self.child_of_child = children_of_child_category
        self.referesh_categories()

    def referesh_categories(self):
        self.category = Category.objects.get(id=self.category.id)
        self.child_category = Category.objects.get(id=self.child_category.id)
        self.child_of_child = Category.objects.get(id=self.child_of_child.id)

    def test_move_root_category_with_children(self):
        staticpage_ct = ContentType.objects.get(model="staticpage")

        self.category.collection = self.collection_B
        self.category.save()

        self.referesh_categories()

        # test change of collection in self and childs
        self.assertEqual(self.category.collection, self.collection_B)
        self.assertEqual(self.child_category.collection, self.collection_B)

        # test added proper content_types to the new collection
        self.assertTrue(staticpage_ct in self.category.collection.content_types.all())

    def test_move_child_category_with_children(self):
        self.assertEqual(self.child_category.get_root(), self.category)
        self.assertTrue(self.child_of_child in self.child_category.get_descendants())

        self.child_category.collection = self.collection_B
        self.child_category.save()

        self.referesh_categories()


        self.assertEqual(self.category.collection, self.collection_A)
        self.assertEqual(self.child_category.collection, self.collection_B)
        self.assertTrue(self.child_category.is_root_node())
        self.assertTrue(self.child_of_child in self.child_category.get_descendants())


class CollectionTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = Collection

    def setUp(self):
        self.test_object = Collection.objects.create(name='An instance')
        self.test_object.save()
        # most views list categories in the collection, so we create one
        cat = Category(name='An instance', collection=self.test_object)
        cat.save()
        frontend.autodiscover()


class MenuItemTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = MenuItem

    def setUp(self):
        menu = Menu.objects.create(name='menu')
        self.test_object = MenuItem(name='An instance', menu=menu)
        self.test_object.save()
        frontend.autodiscover()


class MenuTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = Menu


class TopicTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = Topic

    def setUp(self):
        User = get_model('auth', 'user')
        self.user = User(username='admin')
        self.user.set_password('password')
        self.user.save()
        self.test_object = Topic(name='An instance', author=self.user)
        self.test_object.save()
        frontend.autodiscover()


class FeedTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = Feed

    def setUp(self):
        self.test_object = Feed.objects.create(name="An instance",
                                               url="http://not.existant/rss")
        frontend.autodiscover()


class MultipleFieldTestCase(TestCase):
    def setUp(self):
        class CategoryTeaserListOptions(forms.Form):
            items_per_page = forms.IntegerField(label='Items per page', initial=3, min_value=1)
            labeled = forms.BooleanField(label='Labeled', initial=False, required=False)

        class TestForm(forms.Form):
            field = MultipleField(form=CategoryTeaserListOptions())

        self.form = TestForm()

    def test_initial_values(self):
        self.assertIn('value="3"', self.form.as_p())


class DispatcherTestCase(TestCase):

    def test_unknown_url_returns_404(self):
        # Ticket https://trac.usla.org.ar/cyclope/ticket/43
        self.assertEqual(self.client.get("/category/foo/").status_code, 404)


class TestDemoFixture(TestCase):
    fixtures = ['cyclope_demo.json']

    def test_demo_fixture(self):
        self.assertGreater(Category.objects.count(), 5)
        self.assertGreater(Collection.objects.count(), 3)
        self.assertGreater(MenuItem.objects.count(), 7)


class TestSitemaps(TestCase):

    fixtures = ['cyclope_demo.json']
    sitemaps = [CollectionSitemap, CategorySitemap, MenuSitemap]
    longMessage = False

    def test_sitemap(self):
        for sitemap in self.sitemaps:
            sitemap = sitemap()
            urls = [obj.get("location") for obj in sitemap.get_urls()]
            for url in urls:
                response = self.client.get(url)
                status = response.status_code
                self.assertEqual(status, 200, "Broken url: %s, %d" % (url, status))


class ThemesTestCase(TestCase):

    def test_layout_form(self):
        form = LayoutAdminForm()
        choices = [choice[0] for choice in form.fields["template"].choices]
        self.assertTrue("main.html" in choices)
        self.assertTrue("inner.html" in choices)

    def test_default_themes_integration(self):
        form = SiteSettingsAdminForm()
        choices = [choice[0] for choice in form.fields["theme"].choices]
        self.assertTrue("neutrona" in choices)
        self.assertTrue("frecuency" in choices)

    def test_custom_theme_integration(self):
        form = SiteSettingsAdminForm()
        choices = [choice[0] for choice in form.fields["theme"].choices]
        self.assertTrue("custom_theme" in choices)

    def test_api(self):
        all_themes = themes.get_all_themes()
        theme = all_themes["neutrona"]
        self.assertTrue("main.html" in theme.layout_templates)
        self.assertTrue(theme is themes.get_theme("neutrona"))


#TODO(nicoechaniz)
#class DeleteRelatedContent(TestCase):
#class DeleteFromLayoutsAndMenuItems(TestCase)
