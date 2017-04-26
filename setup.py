#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2013 Código Sur Sociedad Civil
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

import codecs
from setuptools import setup, find_packages

version = '0.4.1.2'


def read(filename):
    return unicode(codecs.open(filename, encoding='utf-8').read())


long_description = '\n\n'.join([read('README.rst'),
                                read('CONTRIBUTORS.rst'),
                                read('CHANGELOG.rst')])

setup(
    name='cyclope3',
    version=version,
    description="CMS for pythonistas who like to code instead of using a web UI for every task.",
    long_description=long_description,
    author='Nicolás Echániz & Santiago Hoerth',
    author_email='nicoechaniz@codigosur.org',
    maintainer='Santiago Piccinini',
    maintainer_email='spiccinini@codigosur.org',
    url='http://forja.codigosur.org/projects/cyclope/',
    license='GPL v3',
    platforms=['OS Independent'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],

    install_requires=[
#        'Django>=1.4,<1.5',
        'Django<1.10',
        'django-autoslug',
        'django-mptt', # 0.4 breaks compatibility
        'django-mptt-tree-editor',
        'Pillow',# python >= 2.6
        'django-simple-captcha',
        'django-filebrowser-nograpup',
#        'South',
        'django-registration',
#        'django-profiles', / deshabiltado ver issue 141
        'django-admin-tools',
        'Whoosh',
        'django-haystack',
        'textile',
        'django-dbgettext',
        'django-rosetta',
        'django-markitup',
        'django-jsonfield',
        'feedparser',
        'django-forms-builder',
#        'django-threadedcomments', deprecado en 1.9 ver issue 138
        'django-crispy-forms',
        'django-compressor',
        'django-generic-ratings',
        'django-activity-stream',
        'python-memcached',
        'pytz',
        'django_markwhat',
#        'django_comments', deprecado en 1.9 ver issue 138
    ],

    scripts=['cyclope/bin/cyclopeproject','cyclope/bin/cyclopedemo'],

    packages=find_packages(),

    include_package_data=True,
    zip_safe=False,
)
