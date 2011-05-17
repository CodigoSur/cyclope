from dbgettext.registry import registry, Options
from dbgettext.lexicons import html
from django.db.models import get_model

from models import Article

class ArticleOptions(Options):
    attributes = ('name',)
    parsed_attributes = {'text': html.lexicon, 'summary':html.lexicon}

    def get_path_identifier(self, obj):
        return obj.slug


registry.register(Article, ArticleOptions)
