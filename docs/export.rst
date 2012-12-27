Fixture creation
================

You could export the data in your project database as a django fixture:

.. code-block:: bash

    python manage.py dumpdata -e admin -e sessions -e contenttypes -e auth -e south -e captcha --natural --indent=2 > initial_data.json

To export group permissions:

.. code-block:: bash

    python manage.py dumpdata auth.group --natural --indent=2 > default_groups.json

