from django import forms
from django.test import TestCase

from widgets import GenericFKWidget
from fields import GenericModelChoiceField


class GenericFKWidgetTest(TestCase):
    def test_inline_rendering(self):
        w = GenericFKWidget("other_type")
        w.render(name="foo-__prefix__-other_object", value=None)
        self.assertEqual(w._test_ct_field, "foo-__prefix__-other_type")
        w = GenericFKWidget("other_type")
        w.render("foo-0-other_object", value=None)
        self.assertEqual(w._test_ct_field, "foo-0-other_type")
        w.render("foo-10-other_object", value=None)
        self.assertEqual(w._test_ct_field, "foo-10-other_type")

class GenericModelChoiceFieldTest(TestCase):
    def test_empty_value(self):
        field = GenericModelChoiceField()
        self.assertRaises(forms.ValidationError, field.validate, u"")
        self.assertRaises(forms.ValidationError, field.to_python, u"")
