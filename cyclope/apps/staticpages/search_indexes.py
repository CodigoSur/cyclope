
from haystack.indexes import *
from haystack import site
import cyclope.apps.staticpages.models


class StaticPageIndex(SearchIndex):
    text = CharField(document=True, use_template=True) #template: summary, text

site.register(cyclope.apps.staticpages.models.StaticPage, StaticPageIndex)
