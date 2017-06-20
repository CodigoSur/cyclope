from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from models import UserProfile

class UserProfilesTestCase(TestCase):
    """Test for django-profiles app incorporated into Cyclope."""
    fixtures = ['simplest_site.json']

    def setUp(self):
        user_model = get_user_model()
        # NOTE usernames with spaces aren't propery reversed
        self.user = user_model.objects.create(username='tico', is_staff=True)
        # uris
        self.create_profile_uri = reverse('profiles_create_profile')
        self.edit_profile_uri = reverse('profiles_edit_profile')
        self.success_url = '/profiles/me/'
        self.profile_detail_uri = reverse('profiles_profile_detail', args=(self.user.username,))
        self.client.force_login(self.user)

    # GET /profiles/create/
    def test_get_create_profile(self):
        response = self.client.get(self.create_profile_uri)
        self.assertEqual(response.status_code, 200)
        # has all fields
        self.assertContains(response, 'id="id_first_name"')
        self.assertContains(response, 'id="id_last_name"')
#        self.assertContains(response, 'id="id_email"') TODO profile with no user (unsaved) shows no user e-mail
        self.assertContains(response, 'id="id_avatar"')
        self.assertContains(response, 'id="id_about"')
        self.assertContains(response, 'id="id_public"')
        # same but user has profile already so gets redirected
        UserProfile.objects.create(user=self.user)
        response = self.client.get(self.create_profile_uri)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.edit_profile_uri)

    # POST /profiles/create/
    def test_post_create_profile(self):
        response = self.client.post(self.create_profile_uri)
        # no field is required, so any post will redirect to success url 
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(response.url, self.success_url)
        self.assertEqual(UserProfile.objects.count(), 1)
        # profile was created so next requests will redirect to edit
        response = self.client.post(self.create_profile_uri)
        self.assertEqual(response.url, self.edit_profile_uri)
        # form validations should respond 200 FIXME no validations at all!
        #UserProfile.objects.all().delete() # ...
        #response = self.client.post(self.create_profile_uri, {"email": "notanemail"})

    # GET /profiles/edit
    def test_get_edit_profile(self):
        response = self.client.get(self.edit_profile_uri)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.create_profile_uri)
        UserProfile.objects.create(user=self.user)
        response = self.client.get(self.edit_profile_uri)
        self.assertEqual(response.status_code, 200)

    # POST /profiles/edit
    def test_post_edit_profile(self):
        response = self.client.post(self.edit_profile_uri)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.create_profile_uri)
        UserProfile.objects.create(user=self.user) # profile created
        response = self.client.post(self.edit_profile_uri)
        self.assertEqual(response.status_code, 200) 

    # GET /profiles/me
    def test_get_me(self):
        # no profile yet
        response = self.client.get('/profiles/me', follow=True)
        self.assertIn(('/profiles/me/', 301), response.redirect_chain) # FIXME why this redirects?
        self.assertIn(('/profiles/create/', 302), response.redirect_chain)
        # profile created
        UserProfile.objects.create(user=self.user)
        response = self.client.get('/profiles/me', follow=True)
        profile_url = self.user.profile.get_absolute_url()
        self.assertIn((profile_url, 302), response.redirect_chain)
    
    # GET /profiles/username
    def test_get_profile_detail(self):
        response = self.client.get(self.profile_detail_uri)
        self.assertEqual(response.status_code, 404)
        # profile created
        UserProfile.objects.create(user=self.user)
        response = self.client.get(self.profile_detail_uri)
        self.assertEqual(response.status_code, 200)
        # unexistent usernames also not found
        fake_profile_detail_uri = reverse('profiles_profile_detail', args=('nonexistent',))
        response = self.client.get(fake_profile_detail_uri)
        self.assertEqual(response.status_code, 404)
    
    def test_auth_permissions(self):
        uris = [self.create_profile_uri, self.edit_profile_uri, self.success_url]
        # we start logged out and with an existent profile
        self.client.logout()
        UserProfile.objects.create(user=self.user)
        for uri in uris:
            response = self.client.get(uri)
            self.assertEqual(response.status_code, 302)
            self.assertIn('/accounts/login', response.url)
        # only profile detail is publicly available
        response = self.client.get(self.profile_detail_uri)
        self.assertEqual(response.status_code, 200)
