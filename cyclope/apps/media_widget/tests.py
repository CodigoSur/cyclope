# -*- coding: utf-8 -*-
"""
jQuery Media Widget tests 
"""

from django.test import TestCase, Client

import os

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from cyclope.apps.articles.models import Article
from cyclope.apps.medialibrary.models import Picture

from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver

class MediaWidgetMixin(object):

    def superuser_create(self): # this could also be a fixture
        self.user = User.objects.create_superuser('john', 'lennon@thebeatles.com', 'johnpassword')

    def superuser_login(self):
        if not hasattr(self, 'user'):
            self.superuser_create()
        self.c.login(username='john', password='johnpassword')
    
    def set_auth_cookie_to_browser(self):
        cookie = self.c.cookies['sessionid']
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh()

class MediaWidgetTests(TestCase, MediaWidgetMixin):

    fixtures = ['simplest_site.json']

    def setUp(self):
        self.c = Client()
        self.PATH =  os.path.dirname(__file__)
        self.FILES_PATH = self.PATH+'/fixtures/files/'

    def test_slugify_uploaded_media_file(self):
        """when uploading files, the file name has to bee slugified to ascii"""
        self.superuser_login()
        test_file = "{}ñuñoa comun.jpg".format(self.FILES_PATH)
        with open(test_file, 'rb') as tf:
            response = self.c.post( reverse('embed-create'), {
                                    'multimedia': tf,
                                    'media_type': 'picture' 
                                    })
            self.assertEqual(response.status_code, 200)                                    
            #tf.close() x multiples post
            #                                          "media_widget_markitup('/media/pictures/2017/02/nunoa-comun.jpg', 'picture', '');"
            self.assertRegexpMatches(response.content, "(media_widget_markitup).+(/media/pictures/).+(nunoa-comun.jpg)")
            # TODO Selenium test JS media_widget_markitup method call, or test responses objects
    
    def test_media_widget_is_reserved_to_staff(self):
        """This is how it is actually used today, however if we used group permissions instead this would have to be expanded."""
        article = Article.objects.create(name='test', text='no,test!')
        art_params = {'article_id': article.pk}
        pic = Picture.objects.create(name='test')
        pic_params = {'pictures_ids': '{},'.format(pic.pk)}
        art_pic_params = art_params.copy()

        urls = [
            ('pictures-upload', art_params, 'get', None),
            ('pictures-new', None, 'get', None), 
            ('pictures-create', art_params, 'post', None),
            ('pictures-update', art_params, 'post', {'picture_id': pic.pk}),
            ('pictures-delete', art_params, 'post', {'picture_id': pic.pk}),
            ('pictures-widget', art_params, 'get', None),
            ('pictures-widget-new', pic_params, 'get', None),
            ('pictures-list', pic_params, 'get', None),
            ('pictures-widget-select', pic_params, 'get', None),
            ('embed-new', {'media_type': 'picture'}, 'get', None),
            ('embed-create', None, 'post', None),
            ('library-fetch', {'media_type': 'picture'}, 'get', None),
        ]
        # NOT LOGGED IN
        for uri, url_params, method, request_params in urls:
            self.assert_login_required(uri, url_params, method, request_params)
        # LOGGED IN
        self.superuser_login()
        for uri, url_params, method, request_params in urls:
            if uri in ('pictures-update', 'pictures-delete'): continue
            self.assert_response_success(uri, url_params, method, request_params)
    
    def assert_login_required(self, uri, url_params, method, request_params):
        response = self.get_response(uri, url_params, method, request_params)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302) # it redirects to admin

    def assert_response_success(self, uri, url_params, method, request_params):
        response = self.get_response(uri, url_params, method, request_params)
        self.assertEqual(response.status_code, 200)
    
    def get_response(self, uri, url_params, method, request_params):
        url = reverse(uri, kwargs=url_params)
        if request_params:
            response = getattr(self.c, method)(url, request_params)
        else:
            response = getattr(self.c, method)(url)
        return response

class MediaWidgetFuncionalTests(LiveServerTestCase, MediaWidgetMixin):
    """Media Widget functional integration tests suite.
       https://docs.djangoproject.com/en/1.10/topics/testing/tools/#django.test.LiveServerTestCase
       Download geckodriver from https://github.com/mozilla/geckodriver/releases
       export PATH=$PATH:/home/numerica/CS/geckodriver 
       Or set yout EXEC_PATH constant below
       """
    fixtures = ['simplest_site.json']       

    EXEC_PATH = '/home/numerica/CS/geckodriver'
    
    @classmethod
    def setUpClass(self):
        super(MediaWidgetFuncionalTests, self).setUpClass()
        self.browser =  webdriver.Firefox(executable_path=self.EXEC_PATH)
        self.browser.implicitly_wait(10)
        self.c = Client()
        
    @classmethod
    def tearDownClass(self):
        super(MediaWidgetFuncionalTests, self).tearDownClass()
        self.browser.quit()

    def test_post_upload_widget_state(self):
        """widget should be refreshed after a succesful upload
           it cannot stay with previously uploaded file state
           mostly when an error was raised (500), it goes unsable."""
        self.superuser_create()
        self.superuser_login()
        self.set_auth_cookie_to_browser()
        self.browser.get('%s%s' % (self.live_server_url, reverse('embed-new', kwargs={'media_type': 'picture'})))

