from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from cyclope.core import frontend

from models import Series
from frontend_views import SeriesDetail
from django.test.client import RequestFactory

class SeriesTest(TestCase):
    def test_content_types(self):
        Series.content_models = [Series]
        ct = ContentType.objects.get_for_model(Series)
        self.assertEqual(Series.get_content_types(), [ct])
    
        self.assertEqual(Series.get_content_models(), [Series]) 
        
        self.assertEqual(Series.get_content_types_choices()[0], ("", '------'))
        self.assertEqual(Series.get_content_types_choices()[1], (ct.id, "series"))
    
    def test_detail_view(self):
        series_detail_view = SeriesDetail()
        series = Series(name="some_series")
        request = RequestFactory().get('/series/some_series')
        request.session = {}
        response = series_detail_view(request=request, content_object=series)
        self.assertContains(response, "some_series", status_code=200)
        self.assertTemplateUsed(response, "base_content_detail.html")
        
        
        
