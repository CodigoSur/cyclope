"""
Example URLConf for a contact form.

Because the ``contact_form`` view takes configurable arguments, it's
recommended that you manually place it somewhere in your URL
configuration with the arguments you want. If you just prefer the
default, however, you can hang this URLConf somewhere in your URL
hierarchy (for best results with the defaults, include it under
``/contact/``).

"""


from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from views import contact_form
from forms import AdminSettingsContactForm

urlpatterns = [
    url(r'^$',
       contact_form,
       {'form_class': AdminSettingsContactForm},
       name='contact_form'),
    url(r'^sent/$',
       TemplateView,
       { 'template': 'contact_form/contact_form_sent.html' },
       name='contact_form_sent'),
]
