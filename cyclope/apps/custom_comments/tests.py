from django.core import mail
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from forms import CustomCommentForm
from models import CustomComment

class CustomCommentTest(TestCase):

    def setUp(self):
        self.site = Site.objects.all()[0]
        self.site.name = "TestSite"
        self.site.domain = "example.com"
        self.site.save()

    def test_suscribe(self):
        comment = CustomComment(name="SAn", email="san@test.com", parent=None,
                                content_object=self.site, site=self.site,
                                subscribe=True)
        comment.save()

        # mail sent to moderators only
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue('New comment on example.com' in mail.outbox[0].subject)


        other_comment = CustomComment(name="SAn", email="san@test.com", parent=None,
                                      content_object=self.site, site=self.site,
                                      subscribe=True)
        other_comment.save()

        reply = CustomComment(name="SAn AE", email="san-ae@test.com", parent=comment,
                              content_object=self.site, site=self.site, subscribe=True)
        reply.save()

        # mail sent to moderators and to original author of first comment
        self.assertEqual(len(mail.outbox), 4)
        self.assertEqual(mail.outbox[3].to[0], "san@test.com")

