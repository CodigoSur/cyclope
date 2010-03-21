#import os
#
## we should consider the security problems of this whole approach
## and evaluate other possibilities.
#def configure(themes_dir):
#    """Reads configuration files for available themes and returns the data in a dictionary.
#    """
#    from django.utils.importlib import import_module
#    import sys, imp
#
#    # skip __init.py and __init__.pyc
#    available_themes = [ item for item in os.listdir(themes_dir) if not item.startswith('__init__.py')]
#
#    sys.path.append(os.path.join(themes_dir, '../'))
#    import themes
#    theme_settings = {}
#    for theme in available_themes:
#        theme_config = import_module("themes.%s" % theme)
#        theme_settings[theme] = theme_config
#        theme_config.templates = ['a','b']
#    return theme_settings
#
#
#def list_templates(theme_name):
#    """Returns a list of the available templates.
#    """
#    import cyclope.settings as cyc_settings
#    from glob import glob
#    themes_dir = cyc_settings.CYCLOPE_THEMES_ROOT
#    tpl_files_path = '%s%s/*.html' % (themes_dir, theme_name)
#    tpl_filenames = map(os.path.basename, glob(tpl_files_path))
#    return tpl_filenames
#
#
#def list_layouts(theme_name):
#    return
#
#def list_regions(theme_name, layout_file):
#    return
