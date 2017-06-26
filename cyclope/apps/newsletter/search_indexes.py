#!/usr/bin/env python
# -*- coding: utf-8 -*-

from haystack import indexes
from cyclope.apps.newsletter.models import Newsletter


class NewsletterIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True) #template: content

    def get_model(self):
        return Newsletter
