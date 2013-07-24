from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from cyclope.core import frontend

from models import Series
from frontend_views import SeriesDetail
from django.test.client import RequestFactory

class ConcreteSeries(Series):
    pass

class SeriesTest(TestCase):
    def test_content_types(self):

        ConcreteSeries.content_models = [ConcreteSeries]
        ct = ContentType.objects.get_for_model(ConcreteSeries)
        self.assertEqual(ConcreteSeries.get_content_types(), [ct])

        self.assertEqual(ConcreteSeries.get_content_models(), [ConcreteSeries])

        self.assertEqual(ConcreteSeries.get_content_types_choices()[0], ("", '------'))
        self.assertEqual(ConcreteSeries.get_content_types_choices()[1], (ct.id, "series"))

    def test_detail_view(self):
        series_detail_view = SeriesDetail()
        series = ConcreteSeries(name="some_series")
        request = RequestFactory().get('/series/some_series')
        request.session = {}
        response = series_detail_view(request=request, content_object=series)
        self.assertContains(response, "some_series", status_code=200)
        self.assertTemplateUsed(response, "base_content_detail.html")
