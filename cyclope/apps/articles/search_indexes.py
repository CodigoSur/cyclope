#!/usr/bin/env python
# -*- coding: utf-8 -*-

from haystack import indexes
from cyclope.apps.articles.models import Article

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True) #template: pretitle, summary, text, author, source
    author = indexes.CharField(model_attr='author', null=True)
    source = indexes.CharField(model_attr='source', null=True)
    pub_date = indexes.DateTimeField(model_attr='creation_date')
    
    def get_model(self):
        return Article
