Changelog for Cyclope 3
=======================

0.2.1 (04-01-2013)
==================

- Added missing locale files to the package

- Fixed reply of threaded comments

- Fixed description of medialibrary teasers not rendering markup


0.2 (27-12-2012)
================

- Added Rating application

- Improved user profiles

- Added user field to BaseContent

- Added cyclopedemo command that creates a new project and loads the demo
  fixtures.

- Replace dependency of FeinCMS by django-mptt-tree-editor.

- Upgraded to django 1.4 (#160).

- Improved comments (#62, #66, #77, #161). Addded threaded comments, comments
  moderation and email notifications.

- Added frontend content edition. Users with permissions on a category now can
  add or edit content from the frontend.

- Added Forms plugin. Now it's posible to create forms from the admin interface.

- Adopt Less CSS `Less CSS <http://lesscss.org/>`_.

- Added Author detail views. This view renders the teasers of it's authored
  content.

- Added Abuse roport plugin.

- Improved backend filters interface (#141). Collection filters are permanent.

- New Slide Show view type.

- Added an image field to Sound Track.

- Improved pagination (added links to first and last page).

- Added view options to collection's category default views.

- Added external syndication/feeds (rss, atom). Now it's posible to show
  external feeds on the site.

- Categories now can be moved from one collection to another.

- Added dynamic sitemap.xml.

- Added 14 new themes.

- Fixed #155 pagination on search not working

- Fixed #164: bug on related content that not validated an empty other_object_id

- Fixed #61: Write a region frontend view to list "last comments"

- Fixed #155: Pagination on search is not working

- Fixed #149: javascript on menu views need fixing.


