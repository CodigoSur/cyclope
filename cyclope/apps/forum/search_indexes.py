#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from haystack import indexes
from cyclope.apps.forum.models import Topic

class TopicIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True) #template: text, author
    pub_date = indexes.DateTimeField(model_attr='creation_date')

    def get_model(self):
        return Topic
