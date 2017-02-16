# -*- coding: utf-8 -*-
"""
jQuery Media Widget tests 
"""

from django.test import TestCase, Client

import os

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver

class MediaWidgetMixin(object):
    def create_test_superuser(self):
        self.user = User.objects.create_superuser('john', 'lennon@thebeatles.com', 'johnpassword')
        
    def superuser_login(self):
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
        self.create_test_superuser()
        self.superuser_login()

    def test_slugify_uploaded_media_file(self):
        """when uploading files, the file name has to bee slugified to ascii"""
        test_file = "{}ñuñoa comun.jpg".format(self.FILES_PATH)
        with open(test_file, 'rb') as tf:
            response = self.c.post( reverse('embed-create'), {
                                    'multimedia': tf,
                                    'media_type': 'picture' 
                                    })
            self.assertEqual(response.status_code, 200)                                    
            #tf.close() x multiples post
            # "media_widget_markitup('/media/pictures/2017/02/nunoa-comun.jpg', 'picture', '');"
            self.assertRegexpMatches(response.content, "(media_widget_markitup).+(/media/pictures/).+(nunoa-comun.jpg)")
            # TODO Selenium test JS media_widget_markitup method call, or test responses objects

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
        self.create_test_superuser()
        self.superuser_login()
        self.set_auth_cookie_to_browser()

    @classmethod
    def tearDownClass(self):
        super(MediaWidgetFuncionalTests, self).tearDownClass()
        self.browser.quit()

    def test_post_upload_widget_state(self):
        """widget should be refreshed after a succesful upload
           it cannot stay with previously uploaded file state
           mostly when an error was raised (500), it goes unsable."""
        self.browser.get('%s%s' % (self.live_server_url, reverse('embed-new', kwargs={'media_type': 'picture'})))
