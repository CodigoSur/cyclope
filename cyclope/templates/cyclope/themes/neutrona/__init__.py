# *-- coding:utf-8 --*
"""Configuration for the Potente theme templates and regions.

Attributes:
    verbose_name: name of theme to be displayed in the admin interface
    layout_templates: dictionary defining regions for the available templates
"""

from django.utils.translation import ugettext_lazy as _

verbose_name = _('Neutrona theme')

layout_templates = {

    'one_sidebar.html':
        {
        'verbose_name': _('One sidebar'),
        'regions' : {
            'header': _('header'),
            'left_sidebar': _('left sidebar'),
            'before_content': _('before content'),
            'after_content': _('after content'),
            'footer': _('footer'),
            }
        },

    'two_sidebars.html':
        {
        'verbose_name': _('Two sidebars'),
        'regions' : {
            'header': _('header'),
            'left_sidebar': _('left sidebar'),
            'right_sidebar': _('right sidebar'),
            'before_content': _('before content'),
            'after_content': _('after content'),
            'footer': _('footer'),
            }
        },
}
