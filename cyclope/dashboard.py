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
        self.columns = 2

        self.children.append(modules.Group(
            title=_('Content'),
            display="tabs",
            draggable = False,
            deletable = False,
            collapsible= False,
            pre_content = _('Create, delete or modify content for your website'),
            children = (
                modules.ModelList(
                    title=_('Main'),
                    include_list=[
                        'cyclope.apps.articles.models.Article',
                        'cyclope.apps.staticpages.models.StaticPage',
                        ]),
                modules.ModelList(
                    title=_('Multimedia Library'),
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
                    include_list=[
                        'cyclope.models.Author',
                        'cyclope.models.Source',
                        ]),
                )))

        self.children.append(modules.ModelList(
            title=_('Categorization'),
            draggable = False,
            deletable = False,
            collapsible= False,
            include_list=[
                'cyclope.core.collections.models.Collection',
                'cyclope.core.collections.models.Category',
                ]))

        self.children.append(modules.ModelList(
            title=_('Site structure'),
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
            draggable = False,
            deletable = False,
            collapsible= False,
            include_list=[
                'cyclope.models.SiteSettings',
                ]))

        self.children.append(modules.ModelList(
            title=_('Comments'),
            pre_content = _('Review and moderate user comments'),
            draggable = False,
            deletable = False,
            collapsible= False,
            include_list=[
                'django.contrib.comments.models.Comment',
                ]))

        self.children.append(modules.AppList(
            title=_('Advanced'),
            draggable = False,
            deletable = False,
            collapsible= False,
            include_list=(
                'django.contrib.sites', 'django.contrib.auth',
                'tagging', 'registration'),
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

        ## append a recent actions module
        #self.children.append(modules.RecentActions(
        #    title=_('Recent Actions'),
        #    limit=5
        #))

        ## append a feed module
        #self.children.append(modules.Feed(
        #    title=_('Latest Django News'),
        #    feed_url='http://www.djangoproject.com/rss/weblog/',
        #    limit=5
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
