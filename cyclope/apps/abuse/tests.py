from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse


import models
from models import AbuseType, AbuseReport, AbuseReportElement
from . import register

register(AbuseType)

class AbuseReportTest(TestCase):
    def setUp(self):
        # Fake sending email
        self.subject, self.message, self.mail_sent = "", "", False

        def mail_managers_fake(subject, message, fail_silently):
            self.subject = subject
            self.message = message
            self.mail_sent = True

        models.mail_managers = mail_managers_fake

        self.abused_object = AbuseType.objects.create(name="abused-object")


        abuse_type = AbuseType.objects.create(name="copyright")
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com',
                                        'johnpassword')

        report_el = AbuseReportElement(abuse_type=abuse_type, user=self.user,
                                       text="Texto del reporte",
                                       content_object=self.abused_object)
        report_el.save()

        self.report_el = report_el
        self.abuse_type = abuse_type

    def test_create_report_element(self):
        self.assertEqual(len(AbuseReport.objects.all()), 1)

    def test_change_status_to_deleted(self):
        report = AbuseReport.objects.get()
        report.status = 'DEL'
        report.save()
        self.assertFalse(AbuseType.objects.filter(name='abused-object').exists())
        report.save()

    def test_send_mail_on_report(self):
        self.assertTrue('abused-object' in self.message)

        report = AbuseReport.objects.get()
        report.status = 'IGN'
        report.save()

        self.mail_sent = False
        other_user = User.objects.create_user('john2', 'lennon@thebeatles.com',
                                              'johnpassword')
        report_el = AbuseReportElement(abuse_type=self.abuse_type,
                                       user=other_user,
                                       text="Texto del reporte 2",
                                       content_object=self.abused_object)
        report_el.save()
        self.assertFalse(self.mail_sent)

    def test_report_abuse(self):
        ct_id = ContentType.objects.get_for_model(self.abused_object).pk
        obj_id = self.abused_object.pk
        self.client.login(username='john', password='johnpassword')
        response = self.client.post(reverse("abuse-report", args=(ct_id, obj_id)))
        self.assertEqual(response.status_code, 200)

    def test_report_loged_in(self):
        ct_id = ContentType.objects.get_for_model(self.abused_object).pk
        obj_id = self.abused_object.pk
        response = self.client.get(reverse("abuse-report", args=(ct_id, obj_id)))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse("abuse-report", args=(ct_id, obj_id)))
        self.assertEqual(response.status_code, 200)

    def test_unique_user_report_for_object(self):
        report_el = AbuseReportElement(abuse_type=self.abuse_type,
                                       user=self.user,
                                       text="Texto del reporte 2",
                                       content_object=self.abused_object)

        self.assertRaises(IntegrityError, report_el.save)


