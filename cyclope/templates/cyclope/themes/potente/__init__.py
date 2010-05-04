# *-- coding:utf-8 --*
"""Configuration for the Potente theme templates and regions.

Attributes:
    verbose_name: name of theme to be displayed in the admin interface
    layout_templates: dictionary defining regions for the available templates
"""

from django.utils.translation import ugettext as _

verbose_name = _('Potente theme')

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

    'sidebar_and_four_panes.html':
        {
        'verbose_name': _('One sidebar and four panes'),
        'regions' : {
            'header': _('header'),
            'sidebar': _('sidebar'),
            'footer': _('footer'),
            'first_pane': _('first pane'),
            'second_pane': _('second pane'),
            'third_pane': _('third pane'),
            'fourth_pane': _('fourth pane'),
            }
        },
}
