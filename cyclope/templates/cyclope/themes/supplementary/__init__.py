# *-- coding:utf-8 --*
"""Configuration for the Neutrona theme templates and regions.

Attributes:
    verbose_name: name of theme to be displayed in the admin interface
    layout_templates: dictionary defining regions for the available templates
"""

from django.utils.translation import ugettext_lazy as _

verbose_name = _('Supplementary')

layout_templates = {

    'four_elements.html':
        {
        'verbose_name': _('Four Elements'),
        'regions' : {
            'air': _('air'),
            'water': _('water'),
            'before_fire': _('before fire'),
            'after_fire': _('after fire'),
            'earth': _('earth'),
            }
        },

    'five_elements.html':
        {
        'verbose_name': _('Five Elements'),
        'regions' : {
            'air': _('air'),
            'water': _('water'),
            'love': _('love'),
            'before_fire': _('before fire'),
            'after_fire': _('after fire'),
            'earth': _('earth'),
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
