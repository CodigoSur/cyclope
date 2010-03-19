from cyclope import settings as cyc_settings

def site_settings(request):
    settings_dict = {}
    for setting in dir(cyc_settings):
        if setting == setting.upper():
            settings_dict[setting] = getattr(cyc_settings, setting)

    return settings_dict
