# -*- coding: utf-8 -*-
"""
jQuery Media Widget tests 
"""

from django.test import TestCase, Client
import os
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class MediaWidgetTests(TestCase):

    fixtures = ['simplest_site.json']

    def setUp(self):
        self.c = Client()
        self.PATH =  os.path.dirname(__file__)
        self.FILES_PATH = self.PATH+'/fixtures/files/'
        self.user = User.objects.create_superuser('john', 'lennon@thebeatles.com', 'johnpassword')
        self.c.login(username='john', password='johnpassword')

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

            # TODO regex here "media_widget_markitup('/media/pictures/2017/02/nunoa-comun.jpg', 'picture', '');"
            self.assertContains(response, "media_widget_markitup('/media/pictures/2017/02/nunoa-comun.jpg', 'picture', '');")

            # TODO Selenium test JS media_widget_markitup method call
