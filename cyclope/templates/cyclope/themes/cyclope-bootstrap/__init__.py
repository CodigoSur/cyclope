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
        'verbose_name': _('Default'),
        'regions' : {
            'header': _('Header'),
            'left': _('Left'),
            'top': _('Top'),
            'bottom': _('Bottom'),
            'footer': _('Footer'),
            }
        },
    'layout_two_columns_right.html':
        {
        'verbose_name': _('Main'),
        'regions' : {
            'header': _('Header'),
            'left': _('Left'),
            'right': _('Right'),
            'top': _('Top'),
            'bottom': _('Bottom'),
            'footer': _('Footer'),
            }
        },
    'layout_three_columns.html':
        {
        'verbose_name': _('Main'),
        'regions' : {
            'header': _('Header'),
            'left': _('Left'),
            'right': _('Right'),
            'top': _('Top'),
            'bottom': _('Bottom'),
            'footer': _('Footer'),
            }
        },
    'layout_one_column.html':
        {
        'verbose_name': _('Main'),
        'regions' : {
            'header': _('Header'),
            'left': _('Left'),
            'right': _('Right'),
            'top': _('Top'),
            'bottom': _('Bottom'),
            'footer': _('Footer'),
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
