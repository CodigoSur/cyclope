from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib import comments
from django.contrib.comments import signals
from django.test.client import RequestFactory

from forms import CustomCommentForm
from models import CustomComment
import models as custom_comment_models
from moderator import CustomCommentModerator, moderator

moderator.register(Site, CustomCommentModerator)

class CustomCommentTest(TestCase):

    def setUp(self):
        self.site = Site.objects.all()[0]
        self.site.name = "TestSite"
        self.site.domain = "example.com"
        self.site.save()
        settings.MANAGERS = ('Manager', 'manager@test.org',)

    def test_suscribe(self):
        CustomComment.moderation_enabled = lambda x:True
        comment = self.create_comment()
        # mail sent to moderators only
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue("New comment posted on '%s'" % self.site in mail.outbox[0].subject)

        other_comment = self.create_comment()

        reply = CustomComment(name="SAn AE", email="san-ae@test.com", parent=comment,
                              content_object=self.site, site=self.site, subscribe=True)
        reply.save()

        # mail sent to moderators and to original author of first comment
        self.assertEqual(len(mail.outbox), 4)
        self.assertEqual(mail.outbox[3].to[0], "san@test.com")

    def test_needs_moderation(self):
        custom_comment_models.moderation_enabled = lambda :False
        self.create_comment()
        self.assertEqual(len(CustomComment.objects.in_moderation()), 0)
        custom_comment_models.moderation_enabled = lambda :True
        self.create_comment()
        self.assertEqual(len(CustomComment.objects.in_moderation()), 1)

    def create_comment(self):
        comment = CustomComment(name="SAn", email="san@test.com", parent=None,
                                content_object=self.site, site=self.site,
                                subscribe=True)

        request = RequestFactory().get('/')

        # Signal that the comment is about to be saved
        responses = signals.comment_will_be_posted.send(
            sender  = comment.__class__,
            comment = comment,
            request = request
        )

        for (receiver, response) in responses:
            if response == False:
                return

        # Save the comment and signal that it was saved
        comment.save()
        signals.comment_was_posted.send(
            sender  = comment.__class__,
            comment = comment,
            request = request
        )
        comment.save()
        return comment

