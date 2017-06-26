#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from haystack import indexes
from cyclope.apps.polls.models import Poll

class PollIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True) #template: name, description
    pub_date = indexes.DateTimeField(model_attr='creation_date')

    def get_model(self):
        return Poll
