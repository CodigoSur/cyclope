#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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

from django.test import TestCase
from django.test.utils import setup_test_environment
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template import TemplateSyntaxError, Template, Context
from django import template

from cyclope.models import SiteSettings, Menu, MenuItem
from cyclope.models import Layout, RegionView, Author
from cyclope.core import frontend
from cyclope.templatetags.cyclope_utils import do_join
from cyclope.apps.staticpages.models import StaticPage
from cyclope.apps.articles.models import Article
from cyclope.apps.medialibrary.models import *

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

def get_content_urls(test_model, test_object=None):
    content_urls = []
    if not test_object:
        test_object = test_model.objects.create(name="something")
    for view in frontend.site._registry[test_model]:
        if not view.is_standard_view:
            continue
        content_urls.append('/'+ test_object.get_instance_url(view.name))
    return content_urls


class SiteSettingsTestCase(TestCase):
    def setUp(self):
        self.site = Site(domain="mydomain.com", name="mydomain")
        self.site.save()

    def test_create_site(self):
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
        site = Site.objects.all()[0]
        site.domain = "localhost:8000"
        site.name = "test domain"
        site.save()

        menu = Menu(name="Main menu", main_menu=True)
        menu.save()

        layout = Layout(name="default", template='one_sidebar.html')
        layout.save()

        menu_item = MenuItem(menu=menu, name="home", site_home=True,
                             active=True, layout=layout)
        menu_item.save()

        site_settings = SiteSettings(site=site,
                                theme="neutrona",
                                default_layout=layout,
                                allow_comments='YES')
        site_settings.save()
        response = self.client.get("/")
        self.assertTemplateUsed(response,
                                u'cyclope/themes/neutrona/one_sidebar.html')
        #TOTO(SAn): add some more usefull asserts

#        export_fixture(['sites','cyclope'],
#            filename='../cyclope/fixtures/simplest_site.json')

    def testBugMenuItemWithoutLayout(self):
        # saving a MenuItem without setting a default site Layout failed
        site = Site(domain="mydomain.com", name="mydomain")
        site.save()
        menu = Menu(name="Main menu", main_menu=True)
        menu.save()
        menu_item = MenuItem(menu=menu, name="home", site_home=True, active=True)
        menu_item.save()

        site_settings = SiteSettings(site=site,
                                theme="neutrona",
                                allow_comments='YES')
        site_settings.save()
        response = self.client.get("/")


    def testSiteWithoutDefaultLayout(self):
        site = Site(domain="mydomain.com", name="mydomain")
        site.save()
        site_settings = SiteSettings(site=site,
                                theme="neutrona",
                                allow_comments='YES')
        site_settings.save()
        response = self.client.get("/")
        self.assertEqual(response.content, 'You need to select a layout for the site')
        #TODO(nicoechaniz): testing for the response content is weak; look for a better option
        # this view should use a standard error template and we should check that the template was used and some message id


    def testSiteWithoutHomeMenuitem(self):
        site = Site(domain="mydomain.com", name="mydomain")
        site.save()
        site_settings = SiteSettings(site=site,
                                theme="neutrona",
                                allow_comments='YES')

        site_settings.save()
        layout = Layout(name="default", template='one_sidebar.html')
        layout.save()
        site_settings.default_layout = layout
        site_settings.save()

        response = self.client.get("/")
        self.assertEqual(response.content, 'The site home page has not been set.')
        #TODO(nicoechaniz): testing for the response content is weak; look for a better option


class RegressionTests(TestCase):

    def setUp(self):
        site = Site(domain="mydomain.com", name="mydomain")
        site.save()
        menu = Menu.objects.create(name="Main menu", main_menu=True)
        menu_item = MenuItem(menu=menu, name="home",
                                            site_home=True, active=True)
        menu_item.save()
        layout = Layout(name="default", template='one_sidebar.html')
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
        layout = Layout.objects.all()[0]
        content_type = ContentType.objects.get(model='staticpage')
        content_view = 'list'
        region = 'header'
        region_view = RegionView(layout=layout, content_type=content_type,
                                 content_view=content_view, region=region)
        region_view.save()
        response = self.client.get("/")
        self.assertContains(response, 'class="regionview staticpage list"', count=1)

    def testAddLayoutRegionViewInstanceViewWithoutContent(self):
        """If the view in a region needs a content object and none is provided
        a template error will be raised when visiting a page using this layout."""
        #TODO(nicoechaniz): this is prevented at admin form level, but should also be checked at data level. See note in forms.py RegionViewInlineForm.clean() method
        layout = Layout.objects.all()[0]
        content_type = ContentType.objects.get(model='staticpage')
        content_view = 'detail'
        region = 'header'
        region_view = RegionView(layout=layout, content_type=content_type,
                                 content_view=content_view, region=region)
        region_view.save()
        self.assertRaises(TemplateSyntaxError, self.client.get, "/")


    def testAddLayoutRegionViewInstanceView(self):
        layout = Layout.objects.get(slug='default')
        region_view = RegionView(layout=layout)
        content_type = ContentType.objects.get(model='staticpage')

        content_view = 'detail'
        static_page = create_static_page(
            name='test add layout region view instance view')
        object_id = static_page.id
        region = 'header'
        region_view = RegionView(
            layout=layout, content_type=content_type, content_view=content_view,
            object_id=object_id, region=region)
        region_view.save()
        response = self.client.get("/")
        self.assertContains(response, 'class="regionview staticpage detail', count=1)

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


class StaticPageTestCase(TestCase):

    def setUp(self):
        frontend.autodiscover()

    def test_creation(self):
        StaticPage.objects.create(name='An instance')
        an_instance = StaticPage.objects.get(slug='an-instance')
        self.assertEqual(an_instance.name, 'An instance')

    def test_content_views(self):
        content_urls = get_content_urls(StaticPage)
        for url in content_urls:
            self.assertEqual(self.client.get(url).status_code, 200)

    def test_region_views(self):
        pass


class ArticleTestCase(TestCase):

    def setUp(self):
        frontend.autodiscover()

    def test_creation(self):
        Article.objects.create(name='An instance')
        an_instance = Article.objects.get(slug='an-instance')
        self.assertEqual(an_instance.name, 'An instance')

    def test_content_views(self):
        content_urls = get_content_urls(Article)
        for url in content_urls:
            self.assertEqual(self.client.get(url).status_code, 200)


class DocumentTestCase(TestCase):
    def setUp(self):
        frontend.autodiscover()

    def test_creation(self):
        Document.objects.create(name='An instance')
        an_instance = Document.objects.get(slug='an-instance')
        self.assertEqual(an_instance.name, 'An instance')

    def test_content_views(self):
        content_urls = get_content_urls(Document)
        for url in content_urls:
            self.assertEqual(self.client.get(url).status_code, 200)


class ExternalContentTestCase(TestCase):
    def setUp(self):
        frontend.autodiscover()

    def test_creation(self):
        ExternalContent.objects.create(name='An instance')
        an_instance = ExternalContent.objects.get(slug='an-instance')
        self.assertEqual(an_instance.name, 'An instance')

    def test_content_views(self):
        content_urls = get_content_urls(ExternalContent)
        for url in content_urls:
            self.assertEqual(self.client.get(url).status_code, 200)


class FlashMovieTestCase(TestCase):
    def setUp(self):
        frontend.autodiscover()

    def test_creation(self):
        FlashMovie.objects.create(name='An instance')
        an_instance = FlashMovie.objects.get(slug='an-instance')
        self.assertEqual(an_instance.name, 'An instance')

    def test_content_views(self):
        flash_object = FlashMovie.objects.create(name="something", flash="/")
        content_urls = get_content_urls(FlashMovie, flash_object)
        for url in content_urls:
            self.assertEqual(self.client.get(url).status_code, 200)


class MovieClipTestCase(TestCase):
    def setUp(self):
        frontend.autodiscover()

    def test_creation(self):
        MovieClip.objects.create(name='An instance')
        an_instance = MovieClip.objects.get(slug='an-instance')
        self.assertEqual(an_instance.name, 'An instance')

    def test_content_views(self):
        content_urls = get_content_urls(MovieClip)
        for url in content_urls:
            self.assertEqual(self.client.get(url).status_code, 200)


class PictureTestCase(TestCase):
    def setUp(self):
        frontend.autodiscover()

    def test_creation(self):
        Picture.objects.create(name='An instance')
        an_instance = Picture.objects.get(slug='an-instance')
        self.assertEqual(an_instance.name, 'An instance')

    def test_content_views(self):
        content_urls = get_content_urls(Picture)
        for url in content_urls:
            self.assertEqual(self.client.get(url).status_code, 200)


class SoundTrackTestCase(TestCase):
    def setUp(self):
        frontend.autodiscover()

    def test_creation(self):
        SoundTrack.objects.create(name='An instance')
        an_instance = SoundTrack.objects.get(slug='an-instance')
        self.assertEqual(an_instance.name, 'An instance')

    def test_content_views(self):
        content_urls = get_content_urls(SoundTrack)
        for url in content_urls:
            self.assertEqual(self.client.get(url).status_code, 200)
