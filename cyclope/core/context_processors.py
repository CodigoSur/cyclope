# *-- coding:utf-8 --*

from cyclope import settings as cyc_settings

def site_settings(request):
    """Exposes all the settings in cyclope.settings to the template.
    """
    settings_dict = {}
    for setting in dir(cyc_settings):
        if setting == setting.upper() and setting.startswith('CYCLOPE'):
            settings_dict[setting] = getattr(cyc_settings, setting)

    return settings_dict
