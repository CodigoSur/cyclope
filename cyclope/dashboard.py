from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard

from cyclope.apps.articles.models import Article

# to activate your index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_INDEX_DASHBOARD = 'cyclope_project.dashboard.CustomIndexDashboard'

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for cyclope_project.
    """
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)
        self.title = _('Site Administration')
        self.columns = 1

        self.children.append(modules.Group(
            title=_('Content'),
            css_classes = ('dbmodule-content', 'main-area-modules',),
            display="tabs",
            draggable = False,
            deletable = False,
            collapsible= False,
            pre_content = _('Create, delete or modify content for your website'),
            children = (
                modules.ModelList(
                    title=_('Main'),
                    css_classes = ('dbmodule-content_main',),
                    include_list=[
                        'cyclope.apps.articles.models.Article',
                        'cyclope.apps.staticpages.models.StaticPage',
                        ]),
                modules.ModelList(
                    title=_('Multimedia Library'),
                    css_classes = ('dbmodule-content_media_library',),
                    include_list=[
                        'cyclope.apps.medialibrary.models.Picture',
                        'cyclope.apps.medialibrary.models.MovieClip',
                        'cyclope.apps.medialibrary.models.SoundTrack',
                        'cyclope.apps.medialibrary.models.Document',
                        'cyclope.apps.medialibrary.models.RegularFile',
                        'cyclope.apps.medialibrary.models.FlashMovie',
                        'cyclope.apps.medialibrary.models.ExternalContent',
                        ]),
                modules.ModelList(
                    title=_('Authors and Sources'),
                    css_classes = ('dbmodule-content_authors_and_sources',),
                    include_list=[
                        'cyclope.models.Author',
                        'cyclope.models.Source',
                        ]),
                )))

        self.children.append(modules.ModelList(
            title=_('Comments'),
            css_classes = ('dbmodule-comments', 'main-area-modules',),
            pre_content = _('Review and moderate user comments'),
            draggable = False,
            deletable = False,
            collapsible= False,
            include_list=[
                'django.contrib.comments.models.Comment',
                ]))

        #self.children.append(modules.ModelList(
        #    title=_('Categorization'),
        #    css_classes = ('dbmodule-categorization', 'main-area-modules',),
        #    pre_content = _('Ordena y clasifica el contenido'),
        #    draggable = False,
        #    deletable = False,
        #    collapsible= False,
        #    include_list=[
        #        'cyclope.core.collections.models.Collection',
        #        'cyclope.core.collections.models.Category',
        #        ]))

        self.children.append(modules.Group(
            title=_('Categorization'),
            css_classes = ('dbmodule-categorization', 'main-area-modules',),
            display="tabs",
            draggable = False,
            deletable = False,
            collapsible= False,
            pre_content = _('Organise and classify the content'),
            children = (
                modules.ModelList(
                    title=_('Collections'),
                    css_classes = ('dbmodule-content_collection',),
                    include_list=[
                       'cyclope.core.collections.models.Collection',
                       'cyclope.core.collections.models.Category',
                        ]),
                modules.ModelList(
                    title=_('Tagging'),
                    css_classes = ('dbmodule-content_tagging',),
                    include_list=[
                        'tagging',
                        ]),
                )))

        self.children.append(modules.ModelList(
            title=_('Site structure'),
            css_classes = ('dbmodule-site_structure', 'main-area-modules',),
            pre_content = _('Configure navigation menu and content blocks position'),
            draggable = False,
            deletable = False,
            collapsible= False,
            include_list=[
                'cyclope.models.Layout',
                'cyclope.models.Menu',
                'cyclope.models.MenuItem',
                ]))

        self.children.append(modules.ModelList(
            title=_('Global settings'),
            css_classes = ('dbmodule-global_settings', 'main-area-modules',),
            draggable = False,
            deletable = False,
            collapsible= False,
            pre_content = _('Cyclope global options'),
            include_list=[
                'cyclope.models.SiteSettings',
                'contact_form.models.ContactFormSettings',
                ]))

        #self.children.append(modules.AppList(
        #    title=_('Advanced'),
        #    css_classes = ('dbmodule-advanced', 'main-area-modules',),
        #    draggable = False,
        #    deletable = False,
        #    collapsible= False,
        #    include_list=(
        #        'django.contrib.sites', 'django.contrib.auth',
        #        'tagging', 'registration'),
        #    ))



        self.children.append(modules.Group(
            title=_('Advanced'),
            css_classes = ('dbmodule-advanced', 'main-area-modules',),
            display="tabs",
            draggable = False,
            deletable = False,
            collapsible= False,
            pre_content = _('Advanced configuration'),
            children = (
                modules.ModelList(
                    title=_('Auth'),
                    css_classes = ('dbmodule-content_auth',),
                    include_list=[
                        'django.contrib.auth',
                        ]),
                modules.ModelList(
                    title=_('Registration'),
                    css_classes = ('dbmodule-content_registration',),
                    include_list=[
                        'registration',
                        ]),
                modules.ModelList(
                    title=_('Sites'),
                    css_classes = ('dbmodule-content_sites',),
                    include_list=[
                        'django.contrib.sites',
                        ]),
                )))


	## RIGHT PANEL MODULES ##

        # append a recent actions module
        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            css_classes = ('dbmodule-recent-actions', 'right-area-modules'),
            draggable = False,
            deletable = False,
            collapsible= False,
            limit=5
        ))

        # append a feed module
        self.children.append(modules.Feed(
            title=_('Codigo Sur, Last News'),
            css_classes = ('dbmodule-feed', 'right-area-modules',),
            draggable = False,
            deletable = False,
            collapsible= False,
            feed_url='http://codigosur.org/rss.php/36',
            limit=6
        ))


        ## append a link list module for "quick links"
        #self.children.append(modules.LinkList(
        #    title=_('Quick links'),
        #    layout='inline',
        #    draggable=False,
        #    deletable=False,
        #    collapsible=False,
        #    children=[
        #        {
        #            'title': _('Return to site'),
        #            'url': '/',
        #        },
        #        {
        #            'title': _('Change password'),
        #            'url': reverse('admin:password_change'),
        #        },
        #        {
        #            'title': _('Log out'),
        #            'url': reverse('admin:logout')
        #        },
        #    ]
        #))



        ## append another link list module for "support".
        #self.children.append(modules.LinkList(
        #    title=_('Support'),
        #    children=[
        #        {
        #            'title': _('Django documentation'),
        #            'url': 'http://docs.djangoproject.com/',
        #            'external': True,
        #        },
        #        {
        #            'title': _('Django "django-users" mailing list'),
        #            'url': 'http://groups.google.com/group/django-users',
        #            'external': True,
        #        },
        #        {
        #            'title': _('Django irc channel'),
        #            'url': 'irc://irc.freenode.net/django',
        #            'external': True,
        #        },
        #    ]
        #))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass


# to activate your app index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'cyclope_project.dashboard.CustomAppIndexDashboard'

class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for cyclope_project.
    """
    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # we disable title because its redundant with the model list module
        self.title = ''

        # append a model list module
        self.children.append(modules.ModelList(
            title=self.app_title,
            include_list=self.models,
        ))

        ## append a recent actions module
        #self.children.append(modules.RecentActions(
        #    title=_('Recent Actions'),
        #    include_list=self.get_app_content_types(),
        #))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass
