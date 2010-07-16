from registration.backends.default import DefaultBackend
from cyclope.forms import RegistrationFormWithCaptcha

class CaptchaBackend(DefaultBackend):

    def get_form_class(self, request):
        """Return a registration with a captcha field."""
        return RegistrationFormWithCaptcha
