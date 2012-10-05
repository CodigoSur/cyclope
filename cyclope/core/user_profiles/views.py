from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required

@login_required
def me(request):
    """
    If profile exists it redirects to the user_profile detail view for the user.
    Redirects to profile creation if it doesn't exist.
    """
    try:
        profile_obj = request.user.get_profile()
        return HttpResponseRedirect(profile_obj.get_absolute_url())
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('profiles_create_profile'))

