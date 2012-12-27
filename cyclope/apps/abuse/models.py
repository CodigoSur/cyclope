from django.db import models, IntegrityError
from django.template.loader import render_to_string
from django.core.mail import mail_managers
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


from . import registry

class AbuseType(models.Model):

    name = models.CharField(_('name'), max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('abuse types')
        verbose_name_plural = _('abuses types')

class AbuseReportElement(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(_('object'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    abuse_type = models.ForeignKey(AbuseType, verbose_name=_('abuse type'))
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)
    report = models.ForeignKey('AbuseReport')

    def __unicode__(self):
        return unicode(self.content_object)

    def save(self, *args, **kwargs):
        if not self.content_type.model_class() in registry:
            raise Exception("Cannot report abuse for %s" % self.content_type)
        report, created = AbuseReport.objects.get_or_create(content_type=self.content_type,
                                                            object_id=self.object_id)
        self.report = report
        super(AbuseReportElement, self).save(*args, **kwargs)

        if self.report.status in ("REP", "HOLD"):
            # send mail to managers
            subject = _("Abuse report for object %s") % self.content_object
            message = render_to_string("abuse/abuse_report_email.txt",
                                      {"element": self,
                                       "domain": Site.objects.get_current().domain})
            mail_managers(subject, message, fail_silently=True)

    class Meta:
        verbose_name = _('abuse report elements')
        verbose_name_plural = _('abuses reports elements')
        unique_together = ("user", "content_type", "object_id")

class AbuseReport(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(_('object'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    status = models.CharField(_('status'), max_length=4,
                                choices = (
                                    ('REP',_('reported')),
                                    ('HOLD',_('on hold')),
                                    ('IGN',_('ignored')),
                                    ('DEL',_('deleted'))
                                ), default='REP')

    def _get_elements(self):
        return AbuseReportElement.objects.filter(content_type=self.content_type,
                                                  object_id=self.object_id)

    def count(self):
        return len(self._get_elements())

    def date(self):
        elem = self._get_elements().order_by('date')[0:1].get()
        return elem.date

    def user(self):
        elem = self._get_elements().order_by('date')[0:1].get()
        return elem.user

    def object(self):
        return self.content_object

    def link(self):
        obj = self.content_object
        return u'<a href="%s">%s</a>' % (obj.get_absolute_url(), obj)

    def __unicode__(self):
        return _("Report: %d") % self.id

    def save(self, *args, **kwargs):
        if AbuseReport.objects.filter(pk=self.pk).exists():
            if self.status == "DEL":
                if self.content_object:
                    if hasattr(self.content_object, 'user'):
                        user = self.content_object.user
                        # TODO
                        user.email_user(subject, message)
                    self.content_object.delete()
                    self.abusereportelement_set.all().delete()
                    self.delete()
                    return

        super(AbuseReport, self).save(*args, **kwargs)

    link.allow_tags = True

    class Meta:
        verbose_name = _('abuse report')
        verbose_name_plural = _('abuses reports')

