from django.db.models import signals

def create_site(app, created_models, verbosity, db, **kwargs):
    from django.contrib.sites.models import Site
    from cyclope.models import Menu, MenuItem, Layout, SiteSettings
    models = (Menu, MenuItem, Layout, SiteSettings)
    if all([model in created_models for model in models]) and \
        not Menu.objects.all():
        # Domain name
        domain = "localhost:8000"
        if kwargs.get('interactive', True):
            msg = "\nDomain name (leave empty for default: %s: " % domain
            input_domain = raw_input(msg)
            domain = input_domain or domain
        # Site name
        site_name = "Cyclope demo"
        if kwargs.get('interactive', True):
            msg = "\nSite name (leave empty for default: %s): " % site_name
            input_name = raw_input(msg)
            site_name = input_name or site_name
        if Site.objects.all():
            site = Site.objects.all()[0]
        else:
            site = Site()
        site.domain = domain
        site.name = site_name
        site.save(using=db)

        menu = Menu(name="Main menu", main_menu=True)
        menu.save(using=db)

        layout = Layout(name="default", template='five_elements.html')
        layout.save(using=db)

        menu_item = MenuItem(menu=menu, name="home", site_home=True,
                             active=True, layout=layout)

        menu_item.save(using=db)

        site_settings = SiteSettings(site=site, theme="neutronix",
                                     default_layout=layout, allow_comments='YES')
        site_settings.save(using=db)

def create_contact_form_settings(app, created_models, verbosity, db, **kwargs):
    from contact_form.models import ContactFormSettings

    if ContactFormSettings in created_models and not ContactFormSettings.objects.all():
        cfs = ContactFormSettings(subject="Contact mail")
        cfs.save(using=db)

def create_user_groups(app, created_models, verbosity, db, **kwargs):
    from django.contrib.auth.models import User, Group
    if User in created_models and Group in created_models:
        for g in ("editors", "managers", "translators"):
            group, created = Group.objects.get_or_create(name=g)
            if created:
                group.save(using=db)


signals.post_syncdb.connect(create_site)

signals.post_syncdb.connect(create_contact_form_settings)

signals.post_syncdb.connect(create_user_groups, dispatch_uid="create_cyclope_user_groups")
