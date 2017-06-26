#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from haystack import indexes
from cyclope.apps.staticpages.models import StaticPage

class StaticPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True) #template: summary, text

    def get_model(self):
        return StaticPage
