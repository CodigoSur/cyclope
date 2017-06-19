"""
Utility functions for retrieving and generating forms for the
site-specific user profile model
adapted from django-profiles 0.2 (https://pypi.python.org/pypi/django-profiles)
since 

"""

from django import forms
from django.contrib.auth.models import SiteProfileNotAvailable
from models import UserProfile

def get_profile_model():
    """
    Return the fixed model class as ``AUTH_PROFILE_MODULE`` setting is deprecated in django 1.7. 
    """
    return UserProfile


def get_profile_form():
    """
    Return a form class (a subclass of the default ``ModelForm``)
    suitable for creating/editing instances of the user
    profile model.
    """
    profile_mod = get_profile_model()
    class _ProfileForm(forms.ModelForm):
        class Meta:
            model = profile_mod
            exclude = ('user',) # User will be filled in by the view.
    return _ProfileForm
