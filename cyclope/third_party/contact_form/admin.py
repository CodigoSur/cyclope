from django.contrib import admin
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from models import ContactFormSettings

class ContactFormSettingsForm(ModelForm):
    class Meta:
        model = ContactFormSettings

    def clean(self):
        data = self.cleaned_data

        if not data['email'] and not data['recipients']:
            raise ValidationError(
                _(u'You have to select at least one recipient or an e-mail \
                    address'))

        return super(ContactFormSettingsForm, self).clean()

class ContactFormSettingsAdmin(admin.ModelAdmin):
    form = ContactFormSettingsForm
    fields =  ('recipients', 'email', 'instructions', 'subject')

admin.site.register(ContactFormSettings, ContactFormSettingsAdmin)
