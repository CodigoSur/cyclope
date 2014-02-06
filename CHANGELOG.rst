Changelog for Cyclope 3
=======================


0.4.1 (5-2-2014)
================

- Improved RSS generation (added publication date)
- Use new version of django-simple-captcha
- Fixed bugs on the Admin for Collection and MenuItem


0.4 (24-9-2013)
===============

- Theme customization. Change fonts, colors and header image from the admin interface.

- Ordered Categorizations. Content on a category can be manualy sorted in the admin.
  Added batch categorization.

- Created Social application. Users of the site now generates activities that another
  users can follow.

- Improved Layout admin page.

- Added Portuguese translation (thanks to Emanuela Castro and Maria Betania Teixeira)

- Improved password reset templates.

- Refactored inter-registration of apps to a new post_init app.

- Improved style of sitemap and comments views

- Big refactoring on tests:

  * Refactored ViewableTestCase to use FrontendView.__call__ instead of doing get(url)
  * Created a TestSuiteRunner to run all cyclope apps tests by default
  * Moved tests from main tests module to app.tests

- As always, a lot of fixes and small improvements.

0.3.1 (10-9-2013)
=================

Mostly bugfix release:

- Refactored inter-registration of apps to a post_init app
- Resolved installation issues

0.3 (24-01-2013)
================

- Improved related contents display: added embedded audio and video player and download links.
  Contribution of Santiago García.

- Enabled "Frontend Edit" on superusers and "managers"

- Reworked Media Player based on MediaElements.js. It now use HTML5 with a Flash fallback.
  File support is  mp3 and ogg for audio, and ogv, mp4, webm and flv for video.
  Contribution of Santiago García.

- Added Network Sharing (using AddThis) capabillities.

- Speed up cyclopeproject and cyclopedemo faking migrations

- Fixed migrations on MySQL

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


