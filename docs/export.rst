Fixture creation
================

You could export the data in your project database as a django fixture:

.. code-block:: bash

    python manage.py dumpdata -e admin -e sessions -e contenttypes -e auth -e south --natural --indent=2 > initial_data.json


