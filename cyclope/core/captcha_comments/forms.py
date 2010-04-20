from django.utils.translation import ugettext as _
from django import forms
from django.contrib.comments.forms import CommentForm
from captcha.fields import CaptchaField

class CommentFormWithCaptcha(CommentForm):
    url = forms.URLField(label=_("Website or Blog"), required=False)
    captcha = CaptchaField(label=_("Security code"))

