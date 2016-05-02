from __future__ import unicode_literals

import sys

from django import forms
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from rgbfield.fields import RGBColorField, RGB_REGEX


class TestRBGColorField(SimpleTestCase):
    def setUp(self):
        self.field = RGBColorField('verbose_name', default='#123445')

    def test_validate_fails(self):
        self.assertRaises(ValidationError, self.field.clean, '', None)
        self.assertRaises(ValidationError, self.field.clean, '12', None)
        self.assertRaises(ValidationError, self.field.clean, '1234', None)
        self.assertRaises(ValidationError, self.field.clean, '00000G', None)
        self.assertRaises(ValidationError, self.field.clean, '#00000G', None)
        self.assertRaises(ValidationError, self.field.clean, '00G', None)
        self.assertRaises(ValidationError, self.field.clean, '#0G', None)
        self.assertRaises(ValidationError, self.field.clean, '#AAAA', None)
        self.assertRaises(ValidationError, self.field.clean, '#1234567', None)

        self.assertRaisesMessage(
            ValidationError,
            'Ensure this value has at most 7 characters (it has 8).',
            self.field.clean, '#1234567', None
        )

    def test_validate_passes(self):
        self.assertEqual('#123445', self.field.clean('#123445', None))
        self.assertEqual('#123', self.field.clean('#123', None))
        self.assertEqual('#ABCDEF', self.field.clean('#ABCDEF', None))
        self.assertEqual('ABCDEF', self.field.clean('ABCDEF', None))
        self.assertEqual('123', self.field.clean('123', None))
        self.assertEqual('ABC', self.field.clean('ABC', None))

    def test_deconstruct(self):
        name, path, args, kwargs = self.field.deconstruct()
        self.assertIsNone(name)
        module, cls = path.rsplit('.', 1)
        field_class = getattr(sys.modules[module], cls)
        field_instance = field_class(*args, **kwargs)
        self.assertIsInstance(field_instance, self.field.__class__)
        self.assertEqual(field_instance.verbose_name, self.field.verbose_name)
        self.assertEqual(field_instance.default, self.field.default)

    def test_formfield(self):
        formfield = self.field.formfield()
        self.assertIsInstance(formfield, forms.RegexField)
        self.assertEqual(formfield.regex, RGB_REGEX)
