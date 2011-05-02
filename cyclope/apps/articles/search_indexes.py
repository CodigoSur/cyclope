#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Código Sur - Nuestra América Asoc. Civil / Fundación Pacificar.
# All rights reserved.
#
# This file is part of Cyclope.
#
# Cyclope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cyclope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from haystack.indexes import *
from haystack import site
import cyclope.apps.articles.models


class ArticleIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True) #template: pretitle, summary, text, author, source
    author = CharField(model_attr='author', null=True)
    source = CharField(model_attr='source', null=True)
    pub_date = DateTimeField(model_attr='creation_date') #TODO: Maybe we have to add 'date'

site.register(cyclope.apps.articles.models.Article, ArticleIndex)
