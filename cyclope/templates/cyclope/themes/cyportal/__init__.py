# *-- coding:utf-8 --*
"""Configuration for the Neutrona theme templates and regions.

Attributes:
    verbose_name: name of theme to be displayed in the admin interface
    layout_templates: dictionary defining regions for the available templates
"""

from django.utils.translation import ugettext_lazy as _

verbose_name = _('Cyportal')

layout_templates = {

    'four_elements.html':
        {
        'verbose_name': _('FourElements'),
        'regions' : {
            'air': _('Air'),
            'water': _('Water'),
            'spark': _('Spark'),
            'ash': _('Ash'),
            'earth': _('Earth'),
            }
        },

    'five_elements.html':
        {
        'verbose_name': _('FiveElements'),
        'regions' : {
            'air': _('Air'),
            'water': _('Water'),
            'love': _('Love'),
            'spark': _('Spark'),
            'ash': _('Ash'),
            'earth': _('Earth'),
            }
        },
    'empty.html':
        {'verbose_name': _('Empty'),
         'regions': {}
         },

    'newsletter.html':
        {'verbose_name': _('Newsletter'),
        'regions' : {
            'header': _('header'),
            'before_content': _('before content'),
            'after_content': _('after content'),
            }
         },
}
