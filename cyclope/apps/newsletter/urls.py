from django.conf.urls import *
from views import preview, send, sent, failed

urlpatterns = patterns(
    '',
    url(r'preview/(?P<id>[\d]+)/$', preview, name='newsletter_preview'),
    url(r'send_test/(?P<id>[\d]+)/$', send, {'test': True},
        name='newsletter_send-test'),
    url(r'send/(?P<id>[\d]+)/$', send, name='newsletter_send'),
    url(r'sent/(?P<id>[\d]+)/$', sent, name='newsletter_sent'),
    url(r'failed/(?P<id>[\d]+)/$', failed, name='newsletter_failed'),
    )
