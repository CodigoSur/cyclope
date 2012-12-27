#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 Código Sur Sociedad Civil.
# All rights reserved.
#
# This file is part of Cyclope.
#
# Cyclope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cyclope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'cyclope_project.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'cyclope_project.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.sites.models import Site

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from contact_form.models import ContactFormSettings

from cyclope.models import SiteSettings
from cyclope.utils import get_singleton

class ModuleNotFound(Exception):
    """Dashboard module not found in dashboard children"""
    def __init__(self, module_title):
        self.title = module_title

    def __str__(self):
        return "Module %s not found in dashboard children" % repr(self.title)

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for cyclope_project.
    """
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)
        self.title = _('Site Administration')
        self.columns = 1

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        user = context.get('user')

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
                        'cyclope.apps.staticpages.models.HTMLBlock',
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

                modules.ModelList(
                    title=_('Comments'),
                    css_classes = ('dbmodule-comments'),
                    #pre_content = _('Review and moderate user comments'),
                    include_list=[
                        'django.contrib.comments.models.Comment',
                    ]),
                )))

        self.children.append(modules.Group(
            title=_('Site structure'),
            css_classes = ('dbmodule-site_structure', 'main-area-modules',),
            pre_content = _('Modify your site layout and collections'),
            display="tabs",
            draggable = False,
            deletable = False,
            collapsible= False,
            children = (

                modules.ModelList(
                    title=_('Collections'),
                    css_classes = ('dbmodule-content_collection',),
                    include_list=[
                       'cyclope.core.collections.models.Collection',
                       'cyclope.core.collections.models.Category',
                        ]),
                modules.ModelList(
                    title=_('Menus'),
                    css_classes = ('dbmodule-menues',),
                    include_list=[
                        'cyclope.models.Menu',
                        'cyclope.models.MenuItem',
                        ]),
                modules.ModelList(
                    title=_('Layouts'),
                    css_classes = ('dbmodule-layout',),
                    include_list=[
                        'cyclope.models.Layout',
                        ]),
               )))


        site_settings = get_singleton(SiteSettings)
        contact_form = get_singleton(ContactFormSettings)

        if user.has_perm('cyclope.change_sitesettings'):
            self.children.append(modules.LinkList(
                    title=_('Global Settings'),
                    css_classes = ('dbmodules-global_settings', 'main-area-modules',),
                    draggable = False,
                    deletable = False,
                    collapsible= False,
                    children=[
                        {'title': _('Site Settings'),
                         'url': '/admin/cyclope/sitesettings/%s/' % site_settings.id,
                         },
                        {'title': _('Contact Form'),
                         'url': '/admin/contact_form/contactformsettings/%s/' % contact_form.id,
                         },
                        ]
                    ),)

        plugins_children = [
            modules.ModelList(
                title=_('Newsletter'),
                css_classes = ('dbmodule-newsletter',),
                include_list=[
                    'cyclope.apps.newsletter.models.Newsletter',
                    ]),
            modules.ModelList(
                title=_('Forms'),
                css_classes = ('dbmodule-forms',),
                include_list=[
                    'forms_builder.forms.models.Form',
                    ]),
            modules.ModelList(
                title=_('Polls'),
                css_classes = ('dbmodule-polls', 'main-area-modules',),
                include_list=[
                    'cyclope.apps.polls.models.Poll',
                    'cyclope.apps.polls.models.Question',
                    ]),
            modules.ModelList(
                title=_('Feeds'),
                css_classes = ('dbmodule-feeds',),
                include_list=[
                    'cyclope.apps.feeds.models.Feed',
                    ]),
            modules.ModelList(
                title=_('Contacts'),
                css_classes = ('dbmodule-contacts', 'main-area-modules',),
                include_list=[
                    'cyclope.apps.contacts.models.Contact',
                    ]),
            modules.ModelList(
                title=_('Abuse'),
                css_classes = ('dbmodule-abuse', 'main-area-modules',),
                include_list=[
                    'cyclope.apps.abuse.models.AbuseType',
                    'cyclope.apps.abuse.models.AbuseReport',
                    ]),
            ]

        self.children.append(modules.Group(
            title=_('Plugins'),
            css_classes = ('dbmodule-plugins', 'main-area-modules',),
            display="tabs",
            draggable = False,
            deletable = False,
            collapsible= False,
            pre_content = (''),
            children = plugins_children
            ))

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
                modules.LinkList(
                    title=_('Site'),
                    css_classes = ('dbmodule-content_sites',),
                    children=[
                        {'title': _('Site'),
                         'url': '/admin/sites/site/%s/' % get_singleton(Site).id,
                         }
                        ]),
                )))

    ## RIGHT PANEL MODULES ##

        ## append a link list module for "quick links"
        quick_links = modules.LinkList(
            title=_('Quick links'),
            css_classes = ('right-area-modules',),
            layout = 'inline',
            draggable = False,
            deletable = False,
            collapsible= False,
            children=[
                {'title': _('Browse media files'),
                 'url': reverse('fb_browse'),
                 },
                {'title': _('Return to site'),
                 'url': '/',
                 'external': True,
                 },
                ]
        )

        # Comments moderation link
        from cyclope.apps.custom_comments import models as custom_comments_models
        if custom_comments_models.moderation_enabled():
            in_moderation = custom_comments_models.CustomComment.objects.in_moderation()
            if in_moderation:
                url = reverse('admin:comments_comment_changelist')
                url +="?is_removed__exact=0&is_public__exact=0"
                moderate_link = {
                    'title': _('%d comments need moderation') % len(in_moderation),
                    'url': url,
                    'external': False,
                }
                quick_links.children.insert(0, moderate_link)

        self.children.append(quick_links)

        # append a recent actions module
        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            css_classes = ('dbmodule-recent-actions', 'right-area-modules'),
            draggable = False,
            deletable = False,
            collapsible= False,
            limit=5,
        ))

        self.children.append(modules.LinkList(
            title=_('Community and support'),
            css_classes = ('right-area-modules',),
            layout = 'inline',
            draggable = False,
            deletable = False,
            collapsible= False,
            children = [
                {
                    'title': _('Official website'),
                    'url': 'http://cyclope.codigosur.org',
                    'external': True,
                    },
                {
                    'title': _('Tutorials'),
                    'url': 'http://tutorialcyclope3.codigosur.net/',
                    'external': True,
                    },
                ]
        ))

        ## append a feed module
        # self.children.append(modules.Feed(
        #    title=_('Codigo Sur, latest news'),
        #    css_classes = ('dbmodule-feed', 'right-area-modules',),
        #    draggable = False,
        #    deletable = False,
        #    collapsible= False,
        #    feed_url='http://codigosur.org/rss.php/36',
        #    limit=6
        #))

    def get_module(self, title):
        """
        Get dashboard module by title.
        """
        for c in self.children:
            if c.title == title:
                return c
        raise ModuleNotFound(title)


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for cyclope_project.
    """
    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            ## modules.RecentActions(
            ##     _('Recent Actions'),
            ##     include_list=self.get_app_content_types(),
            ##     limit=5
            ## )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
