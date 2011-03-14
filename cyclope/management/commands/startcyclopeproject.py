#!/usr/bin/env python
# *-- coding:utf-8 --*

import os
import re
import sys
from random import choice

import django

from django.core import management
from django.core.management.base import copy_helper, CommandError, LabelCommand
from django.utils.importlib import import_module

import cyclope

class Command(LabelCommand):
    help = "Creates a Cyclope project directory structure for the given project name in the current directory."
    args = "[projectname]"
    label = 'project name'

    requires_model_validation = False
    # Can't import settings during this command, because they haven't
    # necessarily been created.
    can_import_settings = False

    def handle_label(self, project_name, **options):
        # Determine the project_name a bit naively -- by looking at the name of
        # the parent directory.
        directory = os.getcwd()

        # Check that the project_name cannot be imported.
        try:
            import_module(project_name)
        except ImportError:
            pass
        else:
            raise CommandError("%r conflicts with the name of an existing Python module and cannot be used as a project name. Please try another name." % project_name)
        # monkeypatch django.__path__ because the internal use in copy_helper
        django_path = django.__path__[:]
        django.__path__[0] = cyclope.__path__[0]
        copy_helper(self.style, 'project', project_name, directory)
        django.__path__ = django_path

        # Create media
        import markitup
        import admin_tools
        import filebrowser
        import feincms
        media = (
            ("admin", os.path.join(django.__path__[0], "contrib", "admin", "media")),
            ("markitup", os.path.join(markitup.__path__[0], "media", "markitup")),
            ("admin_tools", os.path.join(admin_tools.__path__[0], "media", "admin_tools")),
            ("filebrowser", os.path.join(filebrowser.__path__[0], "media", "filebrowser")),
            ("cyclope", os.path.join(cyclope.__path__[0], "media")),
            ("jquery-autocomplete", os.path.join(cyclope.__path__[0], "media", "jquery-autocomplete")),
            ("feincms", os.path.join(cyclope.__path__[0], "media", "feincms")),
        )

        top_dir = os.path.join(directory, project_name)
        media_dir = os.path.join(top_dir, "media")
        os.mkdir(media_dir)
        for name, path in media:
            os.symlink(path, os.path.join(media_dir, name))

        # FIXME: this should not be here
        # Create db
        os.mkdir(os.path.join(top_dir, "db"))

        # Create a random SECRET_KEY hash, and put it in the local settings.
        main_settings_file = os.path.join(directory, project_name, 'local_settings.py')
        settings_contents = open(main_settings_file, 'r').read()
        fp = open(main_settings_file, 'w')
        secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
        settings_contents = re.sub(r"(?<=SECRET_KEY = ')'", secret_key + "'", settings_contents)
        fp.write(settings_contents)
        fp.close()

        print "Now you should run ./manage.py syncdb and then ./manage.py migrate"

if __name__ == "__main__":
    cmnd = Command()
    if len(sys.argv) == 1:
        cmnd.print_help("startcyclopeproject", "")
    else:
        sys.argv.insert(0, "") # Hack run_from_argv
        cmnd.run_from_argv(sys.argv)
