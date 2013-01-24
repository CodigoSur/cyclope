#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 Código Sur Sociedad Civil
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

version = '0.3'


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
        "Development Status :: 4 - Beta",
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

    # revision number is indicated in the dependency_links for packages
    # that are downloaded from source to ensure a tested revision is used.
    dependency_links=[
        'hg+http://bitbucket.org/diegom/django-contact-form#egg=django-contact-form-0.4a1',
        'hg+http://bitbucket.org/nicoechaniz/django-rosetta_temp#egg=django-rosetta-0.6.2-temp',
        'hg+http://bitbucket.org/san/django-jsonfield#egg=django-jsonfield-0.6.0-cyclope',
        'git+http://github.com/HonzaKral/django-threadedcomments.git@issue/39#egg=django-threadedcomments-0.9'
    ],

    install_requires=[
        'Django>=1.4,<1.5',
        'django-autoslug==1.4.1',
        'django-mptt==0.4.2', # 0.4 breaks compatibility
        'django-mptt-tree-editor>=0.1,<0.2',
        'PIL>=1.1.7', # in PIL we trust
        'django-simple-captcha==0.2.0',
        'django-filebrowser-nograpup>=3.0.3,<3.1',
        'South>=0.7,<0.8',
        'django-registration==0.8',
        'django-profiles==0.2',
        'django-admin-tools==0.4.1',
        'django-contact-form>=0.4a1', # installed from our clone
        'Whoosh>=2.4.1,<2.5',
        'django-haystack>=1.2.7,<1.3',
        'textile==2.1.4',
        'django-dbgettext>=0.1',
        'django-rosetta==0.6.2-temp', # installed from our clone
        'django-markitup==1.0',
        'django-jsonfield==0.6.0-cyclope', # installed from our clone
        'feedparser==5.1',
        'django-forms-builder>=0.7.5,<0.8',
        'django-threadedcomments==0.9',
        'django-crispy-forms>=1.2,<1.3',
        'django-compressor>=1.2,<1.3',
        'django-generic-ratings>=0.6,<0.7',
    ],

    scripts=['cyclope/bin/cyclopeproject','cyclope/bin/cyclopedemo'],

    packages=find_packages(),

    include_package_data=True,
    zip_safe=False,
)
