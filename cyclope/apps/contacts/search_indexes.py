#!/usr/bin/env python
# -*- coding: utf-8 -*-

from haystack import indexes
from models import Contact

class ContactIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    given_name = indexes.CharField(model_attr='given_name')
    surname = indexes.CharField(model_attr='surname')
    email = indexes.CharField(model_attr='email')

    def get_model(self):
        return Contact
