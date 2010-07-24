from django.utils.translation import ugettext_lazy as _
from contact_form.forms import AdminSettingsContactForm
from captcha.fields import CaptchaField


class AdminSettingsContactFormWithCaptcha(AdminSettingsContactForm):
    captcha = CaptchaField(label=_("Security code"))
