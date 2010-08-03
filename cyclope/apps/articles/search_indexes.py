
from haystack.indexes import *
from haystack import site
import cyclope.apps.articles.models


class ArticleIndex(SearchIndex):
    text = CharField(document=True, use_template=True) #template: pretitle, summary, text, author, source
    author = CharField(model_attr='author')
    source = CharField(model_attr='source', null=True)
    pub_date = DateTimeField(model_attr='creation_date') #TODO: Maybe we have to add 'date'

site.register(cyclope.apps.articles.models.Article, ArticleIndex)
