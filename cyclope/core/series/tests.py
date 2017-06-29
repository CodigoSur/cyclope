from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from cyclope.core import frontend
from models import Series
from frontend_views import SeriesDetail
from django.test.client import RequestFactory
from django.db import connection

class SeriesTest(TestCase):

    fixtures = ['simplest_site.json']
    
    # this is necessary because Series is an ABSTRACT class so we need to subclass it in order to instance it for tests
    # of course the subclass table does not exist, and it is easier to create it than to make a migration in the test
    # the creation syntax us SQLite specific, though
    def setUp(self):
        connection.cursor().execute("CREATE TABLE series_concreteseries(id INTEGER PRIMARY KEY ASC, name varchar(250), slug varchar(250), published bool, user_id integer, creation_date datetime, modification_date datetime, allow_comments varchar(4), show_author varchar(6), description varchar(250), image varchar(250))")
    def tearDown(self):
        connection.cursor().execute("DROP TABLE series_concreteseries")
    
    def test_content_types(self):
        class ConcreteSeries(Series):
            pass    
        ConcreteSeries.content_models = [ConcreteSeries]
        ct = ContentType.objects.get_for_model(ConcreteSeries)
        self.assertEqual(ConcreteSeries.get_content_types(), [ct])

        self.assertEqual(ConcreteSeries.get_content_models(), [ConcreteSeries])

        self.assertEqual(ConcreteSeries.get_content_types_choices()[0], ("", '------'))
        self.assertEqual(ConcreteSeries.get_content_types_choices()[1], (ct.id, "series"))

    def test_detail_view(self):
        class ConcreteSeries(Series):
            pass    
        series_detail_view = SeriesDetail()
        series = ConcreteSeries(name="some_series")
        request = RequestFactory().get('/concreteseries/some_series')
        request.session = {}
        response = series_detail_view(request=request, content_object=series)
        self.assertContains(response, "some_series", status_code=200)
