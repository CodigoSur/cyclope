# -*- coding: utf-8 -*-
"""
jQuery Media Widget tests 
"""

from django.test import TestCase, Client

import os

from django.core.urlresolvers import reverse

from cyclope.apps.articles.models import Article
from cyclope.apps.medialibrary.models import Picture
import shutil

from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
# waits
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cyclope.utils import FunctionalTestsMixin

class MediaWidgetTests(TestCase, FunctionalTestsMixin):

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
            self.assertRegexpMatches(response.content, "(media_widget_markitup).+(/media/pictures/).+(nunoa-comun).+(.jpg)")
            # TODO test responses context
    
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
    
    # helpers
    
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
        
    def test_upload_files_w_same_name(self):
        """if two files with the same name are uploaded, it should be overwritten.
           this is for URL /media_widget/embed/create"""
        self.superuser_login()
        
        first_file = "{}pic.jpg".format(self.FILES_PATH)
        other_file = "{}otr.jpg".format(self.FILES_PATH)
        placeholder_file = "{}p.jpg".format(self.FILES_PATH)
        
        # upload first file
        with open(first_file, 'rb') as tf:
            self.c.post(reverse('embed-create'), { 'multimedia': tf, 'media_type': 'picture' })
        
        self.assertEqual(Picture.objects.count(), 1)
        
        # backup file in system
        shutil.copy(first_file, placeholder_file)
        # overwrite first file with second
        shutil.copyfile(other_file, first_file)
               
        # upload other file with same name
        with open(first_file, 'rb') as tf:
            self.c.post(reverse('embed-create'), { 'multimedia': tf, 'media_type': 'picture' })

        # each upload creates an object with different paths
        self.assertEqual(Picture.objects.count(), 2)
        pics = Picture.objects.all()
        self.assertNotEqual(pics[0].image.path, pics[1].image.path)
        
        # finally recover first file
        shutil.move(placeholder_file, first_file)

    def test_upload_pictures_w_same_name(self):
        """same as above, but for /media_widget/pictures/create"""
        first_file = "{}pic.jpg".format(self.FILES_PATH)
        other_file = "{}otr.jpg".format(self.FILES_PATH)
        placeholder_file = "{}p.jpg".format(self.FILES_PATH)
        art = Article.objects.create(name='test', text='no,test!')

        self.superuser_login()

        # upload picture to article
        with open(first_file, 'rb') as tf:
            self.c.post(reverse('pictures-create', kwargs={'article_id': art.pk}), { 'image': tf})

        self.assertEqual(Picture.objects.count(), 1)
        
        # backup file in system
        shutil.copy(first_file, placeholder_file)
        # overwrite first file with second
        shutil.copyfile(other_file, first_file)

        # upload other file with same name
        with open(first_file, 'rb') as tf:
            self.c.post(reverse('pictures-create', kwargs={'article_id': art.pk}), { 'image': tf})

        self.assertEqual(Picture.objects.count(), 2)

        # each upload creates an object with different paths
        pics = Picture.objects.all()
        self.assertNotEqual(pics[0].image.path, pics[1].image.path)
        
        # finally recover first file
        shutil.move(placeholder_file, first_file)

    def test_embed_new_picture_redirect(self):
        """ /media_widget/embed/new/None throws DoesNotExist: ContentType matching query does not exist. 
            I have not been able to identify when/why this happens TODO"""
        self.superuser_login()
        wrong_uris = [
            reverse('embed-new',  args=(None,)),
            reverse('embed-new', args=('',))
        ]
        for uri in wrong_uris:
            resp = self.c.get(uri)
        assert True # TODO assertNotRaises...

class MediaWidgetFunctionalTests(LiveServerTestCase, FunctionalTestsMixin):
    """Media Widget functional integration tests suite.
       https://docs.djangoproject.com/en/1.10/topics/testing/tools/#django.test.LiveServerTestCase
       Download geckodriver from https://github.com/mozilla/geckodriver/releases
       export PATH=$PATH:/home/numerica/CS/geckodriver 
       Or set yout EXEC_PATH constant below
       """
    fixtures = ['simplest_site.json']       

    @classmethod
    def setUpClass(self):
        super(MediaWidgetFunctionalTests, self).setUpClass()
        self.browser =  webdriver.Firefox()
        self.browser.implicitly_wait(10)
        self.c = Client()
        self.PATH =  os.path.dirname(__file__)
        self.FILES_PATH = self.PATH+'/fixtures/files/'
        
    @classmethod
    def tearDownClass(self):
        super(MediaWidgetFunctionalTests, self).tearDownClass()
        self.browser.quit()

    def test_post_upload_widget_state(self):
        """widget should be refreshed after a succesful upload
           it cannot stay with previously uploaded file state
           mostly when an error was raised (500), it goes unusable."""
        self.superuser_login_browser()
        time.sleep(1) # wait a sec
        article = Article.objects.create(name='test', text='no,test!')
        self.browser.get('%s/admin/articles/article/%s' % (self.live_server_url, article.pk))
        # poner el puntero en el texto
        textarea = self.browser.find_elements_by_id('id_text')[0]
        textarea.click()
        # levantar el media widget
        widget_button = self.browser.find_elements_by_css_selector('.field-text .markItUpButton20 a')[0]
        widget_button.click()
        # cambiarse al iframe
        frame = self.browser.find_elements_by_css_selector('#media_iframe iframe')[0]
        self.browser.switch_to_frame(1) # self.browser.switch_to(frame)
        multimedia_field = self.browser.find_elements_by_id('id_multimedia')[0]
        multimedia_field.send_keys(self.FILES_PATH+'pic.jpg')
        form = self.browser.find_elements_by_css_selector('form')[0]
        form.submit()
        time.sleep(1) # ajax call not waited
        self.browser.switch_to_default_content()
        self.assertEqual(Picture.objects.count(), 1)
        updated_text = textarea.get_attribute('value') # textarea.text is not updated
        self.assertRegexpMatches(updated_text, "(/media/pictures/).+(pic).+(.jpg)")
        # vuelvo a levantar el media widget
        widget_button = self.browser.find_elements_by_css_selector('.field-text .markItUpButton20 a')[0]
        widget_button.click()
        self.browser.switch_to_frame(1)
        # [] porque no esta activo, si el widget refrezca tiene un nuevo input
        self.assertEqual(len(self.browser.find_elements_by_id("fileName")), 1)

    def test_post_upload_picture_states(self):
        """same as above for pictures widget."""
        article = Article.objects.create(name='test', text='no,test!')
        self.superuser_login_browser()
        time.sleep(3) # wait a sec
        self.browser.get('%s/admin/articles/article/%s' % (self.live_server_url, article.pk))
        # pictures button
        pictures_button = self.browser.find_element_by_id('media_widget_button')
        pictures_button.click()
        # cambiarse al iframe
        frame =  self.browser.find_elements_by_css_selector('#pictures_iframe iframe')[0]
        self.browser.switch_to_frame(frame)
        # submit form
        form = self.browser.find_elements_by_css_selector('form')[0]
        form.submit()
        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.has-error.bg-danger')))
        # resonse 200 empty fielf validation
        self.assertRegexpMatches(self.browser.page_source, 'has-error bg-danger')
        # close button
        self.browser.switch_to_default_content() # close is outside iframe
        close_button = self.browser.find_elements_by_css_selector('.ui-dialog-titlebar-close')[0]
        close_button.click()
        # volver
        pictures_button = self.browser.find_element_by_id('media_widget_button')
        pictures_button.click()
        self.browser.switch_to_frame(frame)
        self.assertNotRegexpMatches(self.browser.page_source, 'has-error bg-danger')

    # TODO
    # def test_post_upload_error_200_state
