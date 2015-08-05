# *-- coding:utf-8 --*
"""Configuration for the Neutrona theme templates and regions.

Attributes:
    verbose_name: name of theme to be displayed in the admin interface
    layout_templates: dictionary defining regions for the available templates
"""

from django.utils.translation import ugettext_lazy as _

verbose_name = _('Cyclope-Bootstrap')

layout_templates = {

    'default.html':
        {
        'verbose_name': _('Default'),
        'regions' : {
            'header': _('Header'),
            'left': _('Left'),
            'right': _('Right'),
            'top': _('Top'),
            'bottom': _('Bottom'),
            'footer': _('Footer'),
            }
        },

    'main.html':
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
    'right': 'sidebar',
    'bottom': '',
}

region_layout_classes = {
    'content': 'jumbotron',
    'header':'',
    'top':'',
    'left': '',
    'right': 'col-xs-4 col-sm-3 col-md-3 col-lg-3',
    'bottom': '',
    'extra_bottom': '',
}

teaser_layout_classes = {
    'content': '',
    'top':'',
    'left': '',
    'right':'',
    'bottom': 'col-xs-12 col-sm-12 col-md-4 col-lg-4',
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
