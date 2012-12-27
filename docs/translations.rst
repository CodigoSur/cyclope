Translations
============

Translations are handled like a normal django application using gettext in 
cyclope/locale directory.

The translation workflow is:

# generate the message file (.po) for the language
# translate the message file (using a simple editor, a program like Lokalize, or
  in _`transifex`)
# generate the compiled messages (.mo)

Generating message files (.po)
------------------------------

In cyclope directory run ``django-admin.py makemessages --locale=es`` to
generate the po file for spanish in ``cyclope/locale/es/LC_MESSAGES/django.po``.


Generate the compiled message files (.mo)
-----------------------------------------

In cyclope directory run ``django-admin.py compilemessages --locale=es``.


External translations
---------------------

When some django app doesn't have a translation or the django's default translation 
for a string isn't correct then an external translation must be done. To that end
theres a file, locale_external/external_translations.py, that holds the external 
strings. So just add there the needed string and makemessages will collect it.


Transifex
---------

To use transifex for translation, first you must upload an updated english POT (default language).
This is the base for translation so the translation strings must be empty.
Generate it with ``django-admin makemessages --locale=en`` and upload it to the resources
edit page https://www.transifex.com/projects/p/django-cyclope/resource/translation/edit/. Doing this
the other languages should be updated with the new strings blank for translation.

Also, if you did a translation for a language offline, you can upload it directly to transifex.

When you finished the translation for a language, download and replace the .po file in locale/LANG and
generate de compiled message file.

The url for the tansifex project is https://www.transifex.com/projects/p/django-cyclope/

