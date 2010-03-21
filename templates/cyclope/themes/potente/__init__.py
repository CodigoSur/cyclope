"""Configuration for the Potente theme templates and regions.

Attributes:
    verbose_name: name of theme to be displayed in the admin interface
    layout_templates: dictionary defining regions for the available templates
"""

from django.utils.translation import ugettext as _

verbose_name = _('potente theme')

layout_templates = {

    'one_sidebar.html':
        {
        'verbose_name': _('One sidebar'),
        'regions' : {
            'header': _('header'),
            'left': _('left'),
            'content': _('content'),
            'footer': _('footer'),
            }
        },

    'two_sidebars.html':
        {
        'verbose_name': _('Two sidebars'),
        'regions' : {
            'header': _('header'),
            'left': _('left'),
            'content': _('content'),
            'right': _('right'),
            'footer': _('footer'),
            }
        },
}
