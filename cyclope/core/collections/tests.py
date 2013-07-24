#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2013 Código Sur Sociedad Civil
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
import json
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from cyclope.tests import ViewableTestCase
from models import Collection, Category, Categorization
from cyclope.apps.articles.models import Article
from cyclope.apps.staticpages.models import StaticPage


class CategoryTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = Category

    def setUp(self):
        super(CategoryTestCase, self).setUp()
        col = Collection.objects.create(name='A collection')
        self.test_object = Category(name='An instance', collection=col)
        self.test_object.save()

    def get_request(self):
        request = RequestFactory().get('/foo/')
        request.session = {}
        request.user, created = User.objects.get_or_create(username='johny')
        return request

class CategorizationOrderTestCase(TestCase):

    def setUp(self):
        self.collection = Collection.objects.create(name='A collection')
        self.collection.content_types.add(ContentType.objects.get(model="staticpage"))
        self.collection.save()
        self.category = Category(name='category foo', collection=self.collection)
        self.category.save()
        self.stpage1 = StaticPage.objects.create(name="static", text="prueba")
        self.stpage2 = StaticPage.objects.create(name="static2", text="prueba")
        self.stpage3 = StaticPage.objects.create(name="static3", text="prueba")

    def test_create_with_order_empty(self):
        ctgz = Categorization(content_object=self.stpage1, category=self.category)
        ctgz.save()
        ctgz2 = Categorization(content_object=self.stpage2, category=self.category)
        ctgz2.save()
        first = self.category.categorizations.all()[0].content_object
        # The default ordering is that the first element corresponds to the last
        # categorization created
        self.assertEqual(first, self.stpage2)

    def test_create_with_order_defined(self):
        ctgz = Categorization(content_object=self.stpage1, category=self.category,
                              order=2)
        ctgz.save()
        ctgz2 = Categorization(content_object=self.stpage2, category=self.category,
                               order=1)
        ctgz2.save()
        first = self.category.categorizations.all()[0].content_object
        self.assertEqual(first, self.stpage2)

    def test_create_with_mixed_order(self):
        "first items are unordered categorizations sorted in creation order"
        ctgz = Categorization(content_object=self.stpage1, category=self.category,
                              order=2)
        ctgz.save()
        ctgz3 = Categorization(content_object=self.stpage3, category=self.category)
        ctgz3.save()
        ctgz2 = Categorization(content_object=self.stpage2, category=self.category)
        ctgz2.save()

        self.category.categorizations.all()[0]
        contents = [c.content_object for c in self.category.categorizations.all()]
        self.assertEqual(contents, [self.stpage2, self.stpage3, self.stpage1])

class MoveCategoryTestCase(TestCase):
    def setUp(self):
        staticpage_ct = ContentType.objects.get(model="staticpage")
        collection_A = Collection.objects.create(name='collection A')
        collection_A.content_types.add(ContentType.objects.get(model="article"))
        collection_A.content_types.add(staticpage_ct)
        collection_A.save()

        collection_B = Collection.objects.create(name='collection B')
        collection_B.content_types.add(ContentType.objects.get(name="article"))
        collection_B.save()

        category = Category(name='Parent', collection=collection_A)
        category.save()

        child_category = Category(name='child', parent=category, collection=collection_A)
        child_category.save()

        children_of_child_category = Category(name='child child',
                                              parent=child_category,
                                              collection=collection_A)
        children_of_child_category.save()

        static_page = StaticPage.objects.create(name="static", text="prueba")
        static_page.categories.create(category=child_category)

        self.collection_A, self.collection_B = collection_A, collection_B
        self.category, self.child_category  = category, child_category
        self.child_of_child = children_of_child_category
        self.referesh_categories()

    def referesh_categories(self):
        self.category = Category.objects.get(id=self.category.id)
        self.child_category = Category.objects.get(id=self.child_category.id)
        self.child_of_child = Category.objects.get(id=self.child_of_child.id)

    def test_move_root_category_with_children(self):
        staticpage_ct = ContentType.objects.get(model="staticpage")

        self.category.collection = self.collection_B
        self.category.save()

        self.referesh_categories()

        # test change of collection in self and childs
        self.assertEqual(self.category.collection, self.collection_B)
        self.assertEqual(self.child_category.collection, self.collection_B)

        # test added proper content_types to the new collection
        self.assertTrue(staticpage_ct in self.category.collection.content_types.all())

    def test_move_child_category_with_children(self):
        self.assertEqual(self.child_category.get_root(), self.category)
        self.assertTrue(self.child_of_child in self.child_category.get_descendants())

        self.child_category.collection = self.collection_B
        self.child_category.save()

        self.referesh_categories()


        self.assertEqual(self.category.collection, self.collection_A)
        self.assertEqual(self.child_category.collection, self.collection_B)
        self.assertTrue(self.child_category.is_root_node())
        self.assertTrue(self.child_of_child in self.child_category.get_descendants())


class CollectionTestCase(ViewableTestCase):
    fixtures = ['simplest_site.json']
    test_model = Collection

    def setUp(self):
        super(CollectionTestCase, self).setUp()
        self.test_object = Collection.objects.create(name='An instance')
        self.test_object.save()
        # most views list categories in the collection, so we create one
        cat = Category(name='A Category', collection=self.test_object)
        cat.save()

    def test_get_widget_ajax(self):
        collection = Collection.objects.get(pk=1)
        response = self.client.get("/collection_categories_json",
                                  {"q": "1"})
        categories = json.loads(response.content)
        self.assertEqual(len(categories), 2)
        self.assertEqual(categories[0]["category_id"], "")
        self.assertEqual(categories[1]["category_id"], 1)
        self.assertContains(response, "A Category")


class CategorizationManagerTests(TestCase):

    def test_get_for_category(self):
        """
        Tests that get_for_category returns the correct elements and making the correct
        number of queries.
        """
        col = Collection.objects.create(name='tema')
        article_ct = ContentType.objects.get(model="article")
        col.content_types.add(article_ct)
        col.save()
        category = Category.objects.create(name='Category', collection=col)
        for n in range(10):
            static_page = StaticPage.objects.create(name="static %d" % n, text="prueba"*100)
            static_page.categories.create(category=category)
            article = Article.objects.create(name="Test article %d" % n, text="prueba"*100)
            article.categories.create(category=category)

        self.assertNumQueries(4, Categorization.objects.get_for_category, category)

        cats = Categorization.objects.get_for_category(category, sort_property="creation_date", reverse=True)
        self.assertEqual(cats[0].content_object, Article.objects.latest("creation_date"))

        cats_random = Categorization.objects.get_for_category(category, sort_property="random")
        self.assertEqual(len(cats), len(cats_random))
