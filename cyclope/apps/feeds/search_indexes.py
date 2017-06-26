#!/usr/bin/env python
# -*- coding: utf-8 -*-

from haystack import indexes
from cyclope.apps.feeds.models import Feed

class FeedIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True) #template: name, summary
    url = indexes.CharField(model_attr='url', null=True)

    def get_model(self):
        return Feed
