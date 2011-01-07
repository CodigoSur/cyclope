from django.db.models import signals
from south.signals import post_migrate
import cyclope

def create_site(app, created_models, verbosity, db, **kwargs):
    from django.contrib.sites.models import Site
    from cyclope.models import Menu, MenuItem, Layout, SiteSettings
    if all([model in created_models for model in (Menu, MenuItem, Layout, SiteSettings)]):
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

        menu = Menu(name="Main menu", main_menu=True)
        menu.save(using=db)

        layout = Layout(name="default", template='one_sidebar.html')
        layout.save(using=db)

        menu_item = MenuItem(menu=menu, name="home", site_home=True,
                             active=True, layout=layout)
        menu_item.save(using=db)

        site_settings = SiteSettings(site=site,
                                theme="neutronica",
                                default_layout=layout,
                                allow_comments='YES')
        site_settings.save(using=db)

def create_user_groups(app, created_models, verbosity, db, **kwargs):
    from django.contrib.auth.models import User, Group
    if User in created_models and Group in created_models:
        for g in ("editors", "managers", "translators"):
            group, created = Group.objects.get_or_create(name=g)
            if created:
                group.save(using=db)


post_migrate.connect(create_site, sender=cyclope)

signals.post_syncdb.connect(create_user_groups, dispatch_uid="create_cyclope_user_groups")
