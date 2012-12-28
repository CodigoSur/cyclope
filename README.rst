Cyclope 3
=========

:synopsys: Cyclope 3 is a django based CMS for pythonistas who don't mind coding a bit and dislike overly-complex user interfaces. It is based on the concept of categorized collections of heterogeneous content types with associated front-end views that can be laid out in the website's page regions. The goal of this project is to create a CMS that is friendly to the end user and versatile for the developer. It won't solve every complex problem at UI level but will let you "expose" the solution.
:copyright: 2010-2012 by `Código Sur Sociedad Civil <http://www.codigosur.org>`_
:url: http://forja.codigosur.org/projects/cyclope
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


Installation
------------

To install in a virtualenv just ``pip install cyclope3``.

For detailed instructions please visit http://forja.codigosur.org/projects/cyclope

Demo project
------------

You can test ``Cyclope`` by running::

 cyclopedemo myproject
 cd myproject
 python manage.py runserver

The admin interface will be accessible at http://localhost:8000/admin and the fronted at: http://localhost:8000

Default username is: admin and the password: password.


Contact and Support
-------------------

If you need to contact the development team you can reach us by e-mail on our `mailing list <http://listas.codigosur.org/mailman/listinfo/cyclopegpl>`_.


