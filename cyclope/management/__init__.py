from django.db.models import signals
import cyclope

def create_site(app, created_models, verbosity, db, **kwargs):
    from django.contrib.sites.models import Site
    from cyclope.models import Menu, MenuItem, Layout, SiteSettings
    if all([model in created_models for model in (Menu, MenuItem, Layout, SiteSettings)]) and \
        not Menu.objects.all():
        msg = "\nDomain name (leave empty for default: localhost:8000): "
        domain = raw_input(msg)
        if not domain:
            domain = "localhost:8000"
        msg = "\nSite name (leave empty for default: cyclope demo): "
        name = raw_input(msg)
        if not name:
            name = "cyclope demo"
        site = Site.objects.all()[0]
        site.domain = domain
        site.name = name
        site.save(using=db)

        menu, created = Menu.objects.get_or_create(name="Main menu", main_menu=True)
        if created:
            menu.save(using=db)

        layout, created = Layout.objects.get_or_create(name="default", template='one_sidebar.html')
        if created:
            layout.save(using=db)

        menu_item, created = MenuItem.objects.get_or_create(menu=menu, name="home",
                                        site_home=True, active=True, layout=layout)
        if created:
            menu_item.save(using=db)

        site_settings, created = SiteSettings.objects.get_or_create(site=site,
                                                                theme="neutronica",
                                                                default_layout=layout,
                                                                allow_comments='YES')
        if created:
            site_settings.save(using=db)

def create_user_groups(app, created_models, verbosity, db, **kwargs):
    from django.contrib.auth.models import User, Group
    if User in created_models and Group in created_models:
        for g in ("editors", "managers", "translators"):
            group, created = Group.objects.get_or_create(name=g)
            if created:
                group.save(using=db)


signals.post_syncdb.connect(create_site)

signals.post_syncdb.connect(create_user_groups, dispatch_uid="create_cyclope_user_groups")
