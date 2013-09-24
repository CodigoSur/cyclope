#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2013 Código Sur Sociedad Civil
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
from django.test.simple import DjangoTestSuiteRunner
from django.test.utils import setup_test_environment
from django.test.client import RequestFactory
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
from cyclope.apps.polls.models import *
from cyclope.apps.forum.models import *
from cyclope.apps.feeds.models import Feed

from cyclope.fields import MultipleField
from cyclope.sitemaps import CollectionSitemap, CategorySitemap, MenuSitemap
from cyclope.forms import (SiteSettingsAdminForm, LayoutAdminForm, MenuItemAdminForm,
                            DesignSettingsAdminForm)
from cyclope import themes
from cyclope import templatetags as cyclope_templatetags
from cyclope.templatetags.cyclope_utils import smart_style

DEFAULT_THEME = "neutronix"
DEFAULT_THEME_REGION = "ash"


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


def get_default_layout():
    if get_default_layout.cache is None:
       get_default_layout.cache = Layout.objects.all()[0]
    return get_default_layout.cache

get_default_layout.cache = None


class CyclopeTestSuiteRunner(DjangoTestSuiteRunner):
    """
    This TestSuiteRunner if fed without app labels runs all the cyclope's apps
    tests. Eg cyclope.core.collection, cyclope.apps.articles, etc.
    """
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        if not test_labels:
            test_labels = ["cyclope"] + [c.split(".")[-1] for c in \
                                         settings.INSTALLED_APPS if "cyclope." in c]
        super(CyclopeTestSuiteRunner, self).run_tests(test_labels, extra_tests,
                                                       **kwargs)


class ViewableTestCase(TestCase):
    """
    Inherit this class to test FrontendViews for a given model.
    """
    fixtures = ['simplest_site.json']
    test_model = None # must be redefined with a model.Model class
    test_object = None

    def setUp(self):
        frontend.autodiscover()

    def test_views(self):
        if self.test_model:
            model_name = self.test_model._meta.module_name
            for view in frontend.site.get_views(self.test_model):

                if view.is_instance_view and self.test_object is None:
                    self.test_object = self.test_model.objects.create(name='An instance')

                if view.is_region_view:
                    add_region_view(self.test_model, view.name, content_object=self.test_object)

                request = self.get_request()

                if view.is_instance_view:
                    response = view(request=request, content_object=self.test_object)
                else:
                    response = view(request=request)

                self.assertEqual(response.status_code, 200)

                if view.is_region_view:
                    self.assertContains(response, 'class="regionview %s %s"' %
                                        (model_name, view.name), count=1)

    def get_request(self):
        request = RequestFactory().get('/foo/')
        request.session = {}
        request.user = AnonymousUser()
        return request



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
        site = Site.objects.get_current()
        menu = Menu.objects.get(main_menu=True)
        menu_item = MenuItem(menu=menu, name="without_layout", active=True)
        menu_item.save()

        site_settings = SiteSettings.objects.get(site=site)
        site_settings.save()
        response = self.client.get("/")


    def testSiteWithoutDefaultLayout(self):
        site = Site.objects.get_current()
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
        static_page = StaticPage.objects.create(
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


class AuthorTestCase(ViewableTestCase):
    test_model = Author

    def setUp(self):
        self.test_object = Author.objects.create(name="An instance")
        article = Article.objects.create(name='Article authored',
                                         author=self.test_object)
        frontend.autodiscover()

    def test_authored_content(self):
        response = self.client.get(u'/author/an-instance/')
        self.assertContains(response, 'An instance')
        self.assertContains(response, 'Article authored')


class MenuItemTestCase(ViewableTestCase):
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
    test_model = Menu


class StaticPageTestCase(ViewableTestCase):
    test_model = StaticPage


class PollTestCase(ViewableTestCase):
    test_model = Poll


class FeedTestCase(ViewableTestCase):
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

    def test_get_widget_ajax(self):
        response = self.client.get("/options_view_widget_html",
                                   {"content_type_name": "category",
                                    "view_name": "default"})
        self.assertContains(response, "view_options")


class CommentsViewsTestCase(ViewableTestCase):
    test_model = django.contrib.comments.get_model()

    def setUp(self):
        site = Site.objects.get_current()
        comment = self.test_model(name="SAn", email="san@test.com", parent=None,
                                  content_object=site, site=site, subscribe=True)
        comment.save()
        self.test_object = comment
        frontend.autodiscover()


class UserProfileViewsTestCase(ViewableTestCase):
    test_model = UserProfile

    def setUp(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        from registration import signals as registration_signals
        registration_signals.user_activated.send(sender=user, user=user)
        self.test_object = user.get_profile()
        frontend.autodiscover()


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
        form = DesignSettingsAdminForm()
        choices = [choice[0] for choice in form.fields["theme"].choices]
        self.assertTrue(DEFAULT_THEME in choices)
        self.assertTrue("frecuency" in choices)

    @unittest.skip("this test fails when there is now custom_theme directory")
    def test_custom_theme_integration(self):
        form = DesignSettingsAdminForm()
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

class LayoutAndRegionsJsonTemplateTagTests(TestCase):
    fixtures = ['simplest_site.json']
    def test_generate_data(self):
        frontend.autodiscover()
        out = Template(
                "{% load layout %}"
                "{% layout_regions_data %}"
            ).render(Context())
        data = json.loads(out)
        self.assertTrue("five_elements.html" in data["layout_templates"])
        self.assertTrue("views_for_models" in data)


