from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist

def staff_required(function=None):
    """
    Decorator for views that checks that the user is staff.
    """
    actual_decorator = user_passes_test(lambda u: u.is_staff)
    if function:
        return actual_decorator(function)
    return actual_decorator


def do_render_object(obj):
    data = []
    data.append('<div class="object-text-repr float-left">%s</div>' % unicode(obj))
    if hasattr(obj, "thumbnail"):
        try:
            data.append(obj.thumbnail())
        except (TypeError, AttributeError) as e:
            pass
    return " ".join(data)


@staff_required
def render_object(request, ct_id, obj_id):
    """
    Returns the html of an arbitrary object to display in the admin FK widget
    via ajax.
    """
    html = ""
    try:
        obj = ContentType.objects.get_for_id(ct_id).get_object_for_this_type(pk=obj_id)
        html = do_render_object(obj)
    except ObjectDoesNotExist:
        pass
    return HttpResponse(html)
