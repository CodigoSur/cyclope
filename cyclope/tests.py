#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 Código Sur Sociedad Civil
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

import time
import json
import unittest
from operator import attrgetter
from collections import defaultdict

from django import forms
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.contrib.sites.models import Site
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template import TemplateSyntaxError, Template, Context
from django import template
from django.db import models
from django.db.models import get_model
import django.contrib.comments

from cyclope.models import SiteSettings, Menu, MenuItem, RelatedContent
from cyclope.models import Layout, RegionView, Author
from cyclope.core import frontend
from cyclope.core.collections.models import *
from cyclope.core.perms.models import CategoryPermission
from cyclope.core.user_profiles.models import UserProfile
from cyclope.templatetags.cyclope_utils import do_join
from cyclope.apps.staticpages.models import StaticPage
from cyclope.apps.articles.models import Article
from cyclope.apps.medialibrary.models import *
from cyclope.apps.polls.models import *
from cyclope.apps.forum.models import *
from cyclope.apps.feeds.models import Feed
from cyclope.apps.dynamicforms.models import DynamicForm

from cyclope.fields import MultipleField
from cyclope.sitemaps import CollectionSitemap, CategorySitemap, MenuSitemap
from cyclope.forms import SiteSettingsAdminForm, LayoutAdminForm, MenuItemAdminForm
from cyclope import themes
from cyclope import templatetags as cyclope_templatetags
from cyclope.templatetags.cyclope_utils import smart_style

DEFAULT_THEME = "neutronix"
DEFAULT_THEME_REGION = "ash"


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
    view = cyclope.core.frontend.site.get_view(model_instance, view_name)

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
    for view in frontend.site.get_views(test_object):
        if view.is_content_view:
            content_urls.append('/'+ get_instance_url(test_object, view.name))
    return content_urls


def get_region_views(test_model):
    return [ view for view in frontend.site.get_views(test_model)
             if view.is_region_view ]

def add_region_view(model, view_name, content_object=None):
    layout = get_default_layout()
    content_type = ContentType.objects.get(model=model._meta.module_name)
    content_view = view_name
    region = DEFAULT_THEME_REGION
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

class FrontendTestCase(TestCase):

    class Model(models.Model):
        name = "Test"

    class ModelDetail(frontend.FrontendView):
        name = 'model-detail'
        verbose_name = 'show a model'
        is_default = True
        is_instance_view = True
        is_region_view = False
        is_content_view = True

    def setUp(self):
        cyclope.core.frontend.site.register_view(self.Model, self.ModelDetail)

    def tearDown(self):
        cyclope.core.frontend.site.unregister_view(self.Model, self.ModelDetail)

    def test_register_view(self):
        view = cyclope.core.frontend.site.get_view(self.Model, 'model-detail')
        self.assertTrue(isinstance(view, self.ModelDetail))

    def test_get_view(self):
        view = cyclope.core.frontend.site.get_view(self.Model, 'model-detail')
        self.assertTrue(isinstance(view, self.ModelDetail))

        # Test with instance
        view = cyclope.core.frontend.site.get_view(self.Model(), 'model-detail')
        self.assertTrue(isinstance(view, self.ModelDetail))

    def test_get_views(self):
        views = cyclope.core.frontend.site.get_views(self.Model())
        self.assertEqual(len(views), 1)
        self.assertTrue(all([isinstance(v, self.ModelDetail) for v in views]))

    def test_unregister(self):
        cyclope.core.frontend.site.register_view(self.Model, self.ModelDetail)
        cyclope.core.frontend.site.unregister_view(self.Model, self.ModelDetail)
        views = cyclope.core.frontend.site.get_views(self.Model())
        self.assertEqual(len(views), 0)

    def test__name__expected(self):
        view = cyclope.core.frontend.site.get_view(self.Model, 'model-detail')
        self.assertEqual(view.__name__, view.name)



class SiteSettingsTestCase(TestCase):
    def setUp(self):
        self.site = Site(domain="mydomain.com", name="mydomain")
        self.site.save()

    def test_creation(self):
        site_settings = SiteSettings(site=self.site,
                                theme=DEFAULT_THEME,
                                allow_comments='YES')
        site_settings.save()
        self.assertEqual(site_settings.site, self.site)

    def test_force_not_deletion(self):
        col = Collection.objects.create(name='A collection')
        layout = Layout.objects.create(name="Test Layout", template='five_elements.html')

        site_settings = SiteSettings(site=self.site, theme=DEFAULT_THEME,
                                     allow_comments='YES',
                                     default_layout=layout,
                                     newsletter_collection=col)
        site_settings.save()

        # On self delete
        site_settings.delete()
        qs = SiteSettings.objects.filter(id=site_settings.id)
        self.assertTrue(len(qs) > 0)

        # On newsletter collection delete
        col.delete()
        qs = SiteSettings.objects.filter(id=site_settings.id)
        self.assertTrue(len(qs) > 0)

        # On layout collection delete
        layout.delete()
        qs = SiteSettings.objects.filter(id=site_settings.id)
        self.assertTrue(len(qs) > 0)


class SiteTestCase(TestCase):
    def testSimplestSite(self):
        """
        Test the simplest creation of a Cyclope-site.
        """
        # Simplest site should be created by syncdb
        response = self.client.get("/")
        self.assertTemplateUsed(response,
                                u'cyclope/themes/neutronix/five_elements.html')

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
        layout = Layout(name="default", template='five_elements.html')
        layout.save()
        site_settings = SiteSettings.objects.create(site=site,
                                theme=DEFAULT_THEME,
                                allow_comments='YES')
        site_settings.default_layout = layout
        site_settings.save()


class RegionViewTestCase(TestCase):
    fixtures = ['simplest_site.json']

    def testAddLayoutRegionView(self):
        layout = get_default_layout()
        content_type = ContentType.objects.get(model='staticpage')
        content_view = 'list'
        region = DEFAULT_THEME_REGION
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
        region = DEFAULT_THEME_REGION
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
        region = DEFAULT_THEME_REGION
        region_view = RegionView(
            layout=layout, content_type=content_type, content_view=content_view,
            object_id=object_id, region=region)
        region_view.save()
        response = self.client.get("/")
        self.assertContains(response, 'class="regionview staticpage detail',
                            count=1)


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


class SiteSearchViewTestCase(TestCase):
    fixtures = ['default_users.json', 'default_groups.json', 'cyclope_demo.json']

    def setUp(self):
        frontend.autodiscover()

    def test_site_search_view(self):
        site = Site.objects.all()[0]
        search_url = ['/search/?q=cyclope']
        for model in frontend.site.base_content_types:
            model_query = "&models=%s.%s" % (model.get_app_label(), model.get_object_name())
            search_url.append(model_query)
        search_url = "".join(search_url)
        response = self.client.get(search_url)
        self.assertContains(response, 'id="search_results"', count=1)


class StaticPageTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = StaticPage


class AuthorTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = Author

    def setUp(self):
        self.test_object = Author.objects.create(name="An instance")
        article = Article.objects.create(name='Article authored',
                                         author=self.test_object)
        frontend.autodiscover()

    def test_authored_content(self):
        content_urls = get_content_urls(self.test_object)
        for url in content_urls:
            response = self.client.get(url)
            self.assertContains(response, 'An instance')
            self.assertContains(response, 'Article authored')


class ArticleTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = Article

    def setUp(self):
        author = Author.objects.create(name="the author")
        self.test_object = Article.objects.create(name='An instance',
                                                  author=author)
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
        cat = Category(name='A Category', collection=self.test_object)
        cat.save()
        frontend.autodiscover()

    def test_get_widget_ajax(self):
        collection = Collection.objects.get(pk=1)
        response = self.client.get("/collection_categories_json",
                                  {"q": "1"})
        categories = json.loads(response.content)
        self.assertEqual(len(categories), 2)
        self.assertEqual(categories[0]["category_id"], "")
        self.assertEqual(categories[1]["category_id"], 1)
        self.assertContains(response, "A Category")


class MenuItemTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = MenuItem

    def setUp(self):
        self.menu = Menu.objects.create(name='menu')
        self.test_object = MenuItem(name='An instance', menu=self.menu)
        self.test_object.save()
        self.article = Article.objects.create(name='An article')
        frontend.autodiscover()

    def test_menu_item_without_view(self):
        self.test_object.content_object = self.article
        self.test_object.save()
        self.assertEqual(self.test_object.content_view,
                         frontend.site.get_default_view_name(Article))

    def test_menu_item_admin_form(self):

        # test without custom_url nor view/content
        self.assertTrue(self.build_admin_form().is_valid())

        # test with custom_url
        self.assertTrue(self.build_admin_form({'custom_url': "/foo/"}).is_valid())


        article_view = frontend.site.get_default_view_name(Article)
        article_ct_pk = ContentType.objects.get(model="article").pk
        # test with content_view
        data = {'content_view': article_view, 'content_type': article_ct_pk,
               'content_object': "%s-%s" % (article_ct_pk, self.article.pk)}
        self.assertTrue(self.build_admin_form(data).is_valid())

        # test fail: requires content_object
        data = {'content_view': article_view, 'content_type': article_ct_pk}
        self.assertFalse(self.build_admin_form(data).is_valid())

        # test fail: can't have custom_url and content
        data = {'custom_url': "/foo/", 'content_type': article_ct_pk}
        self.assertFalse(self.build_admin_form(data).is_valid())

    def test_active_item(self):
        # home menu and An instance menu items
        self.assertEqual(len(frontend.site.get_menuitem_urls()), 2)
        self.test_object.active = False
        self.test_object.save()
        self.assertEqual(len(frontend.site.get_menuitem_urls()), 1)

    def build_admin_form(self, new_data=None):
        base_data = {'menu':self.menu.pk, 'name': 'test_mi'}
        base_data.update(new_data or {})
        return MenuItemAdminForm(base_data)


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
        self.test_object = Topic(name='An instance', user=self.user)
        self.test_object.save()
        frontend.autodiscover()


class FeedTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = Feed

    def setUp(self):
        self.test_object = Feed.objects.create(name="An instance",
                                               url="http://not.existant/rss")
        frontend.autodiscover()


class DynamicFormTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = DynamicForm

    def setUp(self):
        form = DynamicForm.objects.create(title="An instance")
        form.sites.add(Site.objects.get_current())
        form.save()
        form.fields.create(label="field", field_type=1, required=True, visible=True)
        self.test_object = form
        frontend.autodiscover()

    def test_empty_form(self):
        view = frontend.site.get_views(self.test_object)[0]
        url = '/'+ get_instance_url(self.test_object, view.name)
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 200)


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

    def test_get_widget_ajax(self):
        response = self.client.get("/options_view_widget_html",
                                   {"content_type_name": "category",
                                    "view_name": "default"})
        self.assertContains(response, "view_options")


class CommentsViewsTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = django.contrib.comments.get_model()

    def setUp(self):
        site = Site.objects.get_current()
        comment = self.test_model(name="SAn", email="san@test.com", parent=None,
                                  content_object=site, site=site, subscribe=True)
        comment.save()
        self.test_object = comment
        frontend.autodiscover()

    def test_creation(self):
        pass

class UserProfileViewsTestCase(ViewableTestCase):
    test_model = UserProfile

    def setUp(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        from registration import signals as registration_signals
        registration_signals.user_activated.send(sender=user, user=user)
        self.test_object = user.get_profile()
        frontend.autodiscover()

    def test_creation(self):
        pass

class DispatcherTestCase(TestCase):

    def test_unknown_url_returns_404(self):
        # Ticket https://trac.usla.org.ar/cyclope/ticket/43
        self.assertEqual(self.client.get("/category/foo/").status_code, 404)


class TestDemoFixture(TestCase):
    fixtures = ['default_users.json', 'default_groups.json', 'cyclope_demo.json']

    def test_demo_fixture(self):
        self.assertGreater(Category.objects.count(), 1)
        self.assertGreater(Collection.objects.count(), 2)
        self.assertGreater(MenuItem.objects.count(), 6)


class TestSitemaps(TestCase):

    fixtures = ['default_users.json', 'default_groups.json', 'cyclope_demo.json']
    sitemaps = [CollectionSitemap, CategorySitemap, MenuSitemap]
    longMessage = False

    @unittest.skip("this test fails when run on the test suite but not alone")
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
        self.assertTrue("five_elements.html" in choices)
        self.assertTrue("four_elements.html" in choices)

    def test_default_themes_integration(self):
        form = SiteSettingsAdminForm()
        choices = [choice[0] for choice in form.fields["theme"].choices]
        self.assertTrue(DEFAULT_THEME in choices)
        self.assertTrue("frecuency" in choices)

    @unittest.skip("this test fails when there is now custom_theme directory")
    def test_custom_theme_integration(self):
        form = SiteSettingsAdminForm()
        choices = [choice[0] for choice in form.fields["theme"].choices]
        self.assertTrue("custom_theme" in choices)

    def test_api(self):
        all_themes = themes.get_all_themes()
        theme = all_themes[DEFAULT_THEME]
        self.assertTrue("five_elements.html" in theme.layout_templates)
        self.assertTrue(theme is themes.get_theme(DEFAULT_THEME))


class MarkupTestCase(TestCase):

    def timeit(self, test_string):
        start = time.time()
        smart_style(test_string)
        interval = time.time() - start
        return interval

    def test_textile_hang(self):
        WAIT = 0.5
        cyclope_templatetags.cyclope_utils.MARKUP_RENDERER_WAIT = WAIT
        cyclope_templatetags.cyclope_utils.lru_cache.size_limit = 2

        foo_string = "foo" * 10000
        bar_string = "bar" * 10000

        self.assertTrue(self.timeit(foo_string) > WAIT) # non cached version
        self.assertTrue(self.timeit(foo_string) < WAIT) # cached version

        self.assertTrue(self.timeit(bar_string) > WAIT) # non cached version
        self.assertTrue(self.timeit(bar_string) < WAIT) # cached version

        self.assertTrue(self.timeit(foo_string) < WAIT) # cached version
        """
        for i in range(1, 5):
            print self.timeit("baz"*i*10000)
        for i in range(1, 5)[::-1]:
            print self.timeit("baz"*i*10000)
        """
        self.timeit("baz") # bar_string should fallen from the cache
        self.assertTrue(self.timeit(foo_string) > WAIT) # non cached version


class RelatedContentTestCase(TestCase):

    def setUp(self):
        self.article = Article.objects.create(name="Article")
        self.related_article = Article.objects.create(name="Article Related")

    def test_create_related(self):
        rc = RelatedContent.objects.create(self_object=self.article,
                                           other_object=self.related_article)
        self.assertEqual(self.article.related_contents.get().other_object,
                         self.related_article)

    def test_delete_relatedcontent_forward(self):
        """
        Tests deletion of RelatedContent objects when the self's related content
        is deleted.
        """
        rc = RelatedContent.objects.create(self_object=self.article,
                                           other_object=self.related_article)

        self.assertEqual(RelatedContent.objects.count(), 1)
        self.article.delete()
        self.assertEqual(RelatedContent.objects.count(), 0)

    def test_delete_relatedcontent_backward(self):
        """
        Tests deletion of RelatedContent objects when the other related content
        is deleted.
        """
        rc = RelatedContent.objects.create(self_object=self.article,
                                           other_object=self.related_article)

        self.assertEqual(RelatedContent.objects.count(), 1)
        self.related_article.delete()
        self.assertEqual(RelatedContent.objects.count(), 0)


class DeleteFromLayoutsAndMenuItems(TestCase):
    def setUp(self):
        MenuItem.objects.all().delete()

    def test_deletion(self):
        frontend.autodiscover()
        article = Article.objects.create(name="Article")

        layout = get_default_layout()
        region_view = RegionView(layout=layout)
        article_ct = ContentType.objects.get_for_model(article)
        region_view = RegionView.objects.create(content_object=article,
                                                layout=layout,
                                                content_view="detail")

        menu = Menu.objects.create(name='menu')
        mi = MenuItem(name='article item', menu=menu, content_object=article,
                      content_view="detail")
        mi.save()

        self.assertEqual(RegionView.objects.count(), 1)
        self.assertEqual(MenuItem.objects.get().content_object, article)
        article.delete()
        self.assertEqual(RegionView.objects.count(), 0)
        self.assertEqual(MenuItem.objects.get().content_object, None)


class FrontendEditTestCase(TestCase):
    fixtures = ['simplest_site.json']

    def setUp(self):
        self.article = Article.objects.create(name='Article')
        self.perm_user = User(username='perm_user', is_staff=True)
        self.perm_user.set_password('password')
        self.perm_user.save()
        self.non_perm_user = User(username='non_perm_user', is_staff=True)
        self.non_perm_user.set_password('password')
        self.non_perm_user.save()
        self.anonymous_user = AnonymousUser()
        col = Collection.objects.create(name='Collection')
        col.content_types.add(ContentType.objects.get(model="article"))
        col.save()
        self.category = Category(name='Category', collection=col)
        self.category.save()
        categorization = Categorization(category=self.category, content_object=self.article)
        self.article.categories.add(categorization)
        perm = CategoryPermission(user=self.perm_user, category=self.category,
                                  can_edit_content=True, can_add_content=True)
        perm.save()

        frontend.autodiscover()

    def test_add_content_perm(self):
        self.assertTrue(self.perm_user.has_perm('add_content', self.category))
        self.assertFalse(self.non_perm_user.has_perm('add_content', self.category))
        self.assertFalse(self.anonymous_user.has_perm('add_content', self.category))

    def test_edit_content_perm(self):
        self.assertTrue(self.perm_user.has_perm('edit_content', self.article))
        self.assertFalse(self.non_perm_user.has_perm('add_content', self.article))
        self.assertFalse(self.anonymous_user.has_perm('add_content', self.article))

    def test_edit_link(self):
        response = self.client.get('/article/article/')
        self.assertNotContains(response, 'class="edit_link"')

        self.client.login(username='perm_user', password='password')
        response = self.client.get('/article/article/')
        self.assertContains(response, 'class="edit_link"', count=1)

        self.client.login(username='non_perm_user', password='password')
        response = self.client.get('/article/article/')
        self.assertNotContains(response, 'class="edit_link"')

    def test_add_content_link(self):
        response = self.client.get('/category/category/')
        self.assertNotContains(response, 'class="category_add_content"')

        self.client.login(username=self.perm_user.username, password='password')
        response = self.client.get('/category/category/')
        self.assertContains(response, 'class="category_add_content"', count=1)

        self.client.login(username=self.non_perm_user.username, password='password')
        response = self.client.get('/category/category/')
        self.assertNotContains(response, 'class="category_add_content"')

class SimpleAdminTests(TestCase):
    """
    This is a realy simple test to catch errors on GET of some pages of the
    admin.
    """
    fixtures = ['default_users.json', 'default_groups.json', 'cyclope_demo.json']

    pages = [
        "/admin/",
        "/admin/cyclope/menuitem/", "/admin/cyclope/menuitem/1/",
        "/admin/cyclope/menu/", "/admin/cyclope/menu/1/",
        "/admin/cyclope/layout/", "/admin/cyclope/layout/1/",
        "/admin/collections/collection/", "/admin/collections/collection/1/",
        "/admin/collections/category/", "/admin/collections/category/1/",
        "/admin/articles/article/", "/admin/articles/article/1/",
        "/admin/cyclope/sitesettings/1/",
    ]

    def test_get_some_pages(self):
        admin = User.objects.get(username='admin')
        self.client.login(username='admin', password="password")
        for page in self.pages:
            status = self.client.get(page).status_code
            self.assertEqual(status, 200, "status: %d | page: %s" % (status, page))


class CategorizationManagerTests(TestCase):

    def test_get_for_category(self):
        """
        Tests that get_for_category returns the correct elements and making the correct
        number of queries.
        """
        col = Collection.objects.create(name='tema')
        article_ct = ContentType.objects.get(model="article")
        col.content_types.add(article_ct)
        col.save()
        category = Category.objects.create(name='Category', collection=col)
        for n in range(10):
            static_page = StaticPage.objects.create(name="static %d" % n, text="prueba"*100)
            static_page.categories.create(category=category)
            article = Article.objects.create(name="Test article %d" % n, text="prueba"*100)
            article.categories.create(category=category)

        self.assertNumQueries(4, Categorization.objects.get_for_category, category)

        cats = Categorization.objects.get_for_category(category, sort_property="creation_date", reverse=True)
        self.assertEqual(cats[0].content_object, Article.objects.latest("creation_date"))

        cats_random = Categorization.objects.get_for_category(category, sort_property="random")
        self.assertEqual(len(cats), len(cats_random))



class GetSingletonTests(TestCase):
    def test_get_singleton(self):
        from cyclope.utils import get_singleton
        site_settings = get_singleton(SiteSettings)
        site_settings.allow_comments = "YES"
        site_settings.save()
        site_settings = get_singleton(SiteSettings)
        self.assertEqual(site_settings.allow_comments, "YES")

        site_settings.allow_comments = "NO"
        site_settings.save()
        site_settings = get_singleton(SiteSettings)
        self.assertEqual(site_settings.allow_comments, "NO")
