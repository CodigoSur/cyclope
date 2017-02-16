# -*- coding: utf-8 -*-
"""
jQuery Media Widget tests 
"""

from django.test import TestCase, Client
import os
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from cyclope.apps.articles.models import Article

class MediaWidgetTests(TestCase):

    fixtures = ['simplest_site.json']

    # this could also be a fixture
    def superuser_create(self):
        self.user = User.objects.create_superuser('john', 'lennon@thebeatles.com', 'johnpassword')

    def superuser_login(self):
        if not hasattr(self, 'user'):
            self.superuser_create()
        self.c.login(username='john', password='johnpassword')

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
            # "media_widget_markitup('/media/pictures/2017/02/nunoa-comun.jpg', 'picture', '');"
            self.assertRegexpMatches(response.content, "(media_widget_markitup).+(/media/pictures/).+(nunoa-comun.jpg)")
            # TODO Selenium test JS media_widget_markitup method call
    
    def test_media_widget_is_reserved_to_staff(self):
        """This is how it is actually used today, however if we used group permissions instead this would have to be expanded."""
        article = Article.objects.create(name='test', text='no,test!')
        # NOT LOGGED IN
        urls = [
            ('pictures-new', None), 
            ('pictures-upload', {'article_id': article.pk})
        ]
        for url, params in urls:
            self.assert_login_required(url, params)
        # LOGGED IN
        self.superuser_login()
        for url, params in urls:
            self.assert_response_success(url, params)
    
    def assert_response_success(self, url, params):
        """params is a dict"""
        response = self.c.get(reverse(url, kwargs=params))
        self.assertEqual(response.status_code, 200)

    def assert_login_required(self, url, params):
        response = self.c.get(reverse(url, kwargs=params))
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302) # it redirects to admin
    
