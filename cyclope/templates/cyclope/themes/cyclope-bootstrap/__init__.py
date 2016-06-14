# *-- coding:utf-8 --*
"""Configuration for the Neutrona theme templates and regions.

Attributes:
    verbose_name: name of theme to be displayed in the admin interface
    layout_templates: dictionary defining regions for the available templates
"""

from django.utils.translation import ugettext_lazy as _

verbose_name = _('Cyclope-Bootstrap')
theme_type = 'bootstrap'

layout_templates = {

    'layout_two_columns_left.html':
        {
        'verbose_name': _('Two columns Left'),
        'regions' : {
            'header': {'name': _('Header'), 'weight': 1},
            'left': {'name': _('Left'), 'weight': 2},
            'top': {'name': _('Top'), 'weight': 3},
            'bottom': {'name': _('Bottom'), 'weight': 4},
            'footer': {'name': _('Footer'), 'weight': 5}
            }
        },
    'layout_two_columns_right.html':
        {
        'verbose_name': _('Two columns Right'),
        'regions' : {
            'header': {'name': _('Header'), 'weight': 1},
            'right': {'name': _('Right'), 'weight': 4},
            'top': {'name': _('Top'), 'weight': 2},
            'bottom': {'name': _('Bottom'), 'weight': 3},
            'footer': {'name': _('Footer'), 'weight': 5},
            }
        },
    'layout_three_columns.html':
        {
        'verbose_name': _('Three columns'),
        'regions' : {
            'header': {'name': _('Header'), 'weight': 1},
            'left': {'name': _('Left'), 'weight': 2},
            'right': {'name': _('Right'), 'weight': 5},
            'top': {'name': _('Top'), 'weight': 3},
            'bottom': {'name': _('Bottom'), 'weight': 4},
            'footer': {'name': _('Footer'), 'weight': 6}
            }
        },
    'layout_one_column.html':
        {
        'verbose_name': _('One column'),
        'regions' : {
            'header': {'name': _('Header'), 'weight': 1},
            'top': {'name': _('Top'), 'weight': 2},
            'bottom': {'name': _('Bottom'), 'weight': 3},
            'footer': {'name': _('Footer'), 'weight': 4}
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

region_layout_ids = {
    'content': '',
    'top': '',
    'left': '',
    'right': '',
    'bottom': '',
}

region_layout_classes = {
    'content': '',
    'header':'',
    'top':'',
    'left': '',
    'right': '',
    'bottom': '',
    'extra_bottom': '',
}

teaser_layout_classes = {
    'content': '',
    'top':'',
    'left': '',
    'right':'',
    'bottom': '',
}

inline_content_classes = {
    'content': '',
    'header':'',
    'top':'',
    'left': '',
    'right': '',
    'bottom': '',
    'extra_bottom': '',
}
