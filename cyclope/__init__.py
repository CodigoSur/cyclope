# -*- coding: utf-8 -*-

"""
What is Cyclope
===============

:synopsys: ``Cyclope`` is a `Django`_ based CMS. It is built around the idea of collections of categorized content objects which can be displayed using different associated views.
:copyright: 2010 by `Código Sur <http://www.codigosur.org>`_ -  Nuestra América Asoc. Civil / Fundación Pacificar
:authors: Nicolás Echániz, Santiago Hoerth (see AUTHORS.txt for a full list of contributors)
:url: http://bitbucket.org/nicoechaniz/django-cyclope/
:version: 0.1.0
:licence: GPL v3

Target audience
---------------

``Cyclope`` is developed with three different audiences in mind:

1. Developers:

    We created ``Cyclope`` thinking of those developers that actually like to code in their language of choice: Python. They don't really look for a product that will let them accomplish even the most complex stuff from a web-based UI.

    We just aim at providing developers with the tools necessary to easily expose their content types and views for site managers to work with in the admin interface.

    Custom created content types and views can easily be packed in modules for drop-in re-utilization.

2. Site managers:

    They will use the Django admin interface to set up the website global settings, theme, layouts, menus, and categories.

3. Content editors:

    Will have access to a customized Django admin interface to create categories and content for the different content types and collections available in the website.


Documentation
-------------
...

Installation
------------
...


Demo project
------------

You can test ``Cyclope`` by running: :command:`python manage.py runserver` in the provided cyclope_demo/ folder.

The admin interface will be accessible at http://localhost:8000/admin and the fronted at: http://localhost:8000

Default username is: admin and the password: password.


Contact and Support
-------------------

If you need to contact the development team you can reach us by e-mail: nicoechaniz@codigosur.org


"""

VERSION = (0, 1, 0)
__version__ = '.'.join(map(str, VERSION))

# We import site settings as FeinCMS does
# not using Django settings at module level
# this allows us to import cyclope in setup.py
# but breaks automatica of update dynamic settings
# see TODO note in default_settings.py
from django.utils.functional import LazyObject

class LazySettings(LazyObject):
    def _setup(self):
        from cyclope import default_settings
        self._wrapped = Settings(default_settings)

class Settings(object):
    def __init__(self, settings_module):
        for setting in dir(settings_module):
            if setting == setting.upper():
                setattr(self, setting, getattr(settings_module, setting))

settings = LazySettings()
