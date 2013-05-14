
from django.dispatch import Signal

# This signal is fired when a BaseContent object is created on the admin
admin_post_create = Signal(providing_args=["request", "instance"])
