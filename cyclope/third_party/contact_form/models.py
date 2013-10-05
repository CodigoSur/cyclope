from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class ContactFormSettings(models.Model):
    recipients =  models.ManyToManyField(User, null=True, blank=True,
                                         limit_choices_to = {'is_staff':True},
                                         verbose_name = _('Recipients'))

    email = models.EmailField(_('E-mail'), blank=True,
                  help_text = (_('Destination e-mail address. You have to \
                  select at least one recipient or an e-mail address')))
    subject = models.CharField(_('E-mail subject'), max_length=100, blank=False)
    instructions = models.TextField(_('Message to show before the form'),
                                     blank=True)

    def __unicode__(self):
        return u'%s' % (_('Contact form settings'))

    class Meta:
        verbose_name = _('Contact form settings')
        verbose_name_plural = _('Contact form settings')
