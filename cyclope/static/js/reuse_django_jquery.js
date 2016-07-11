// jQuery is already loaded by the admin, but into the django namespace. This way we avoid loading jQuery again.

var jQuery = django.jQuery
var $ = jQuery
