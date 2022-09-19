from django.test import TestCase
from weatherapp.forms import CityForm, EMPTY_CITY_ERROR

class CityFormTest(TestCase):
    '''тест формы для города'''

    def test_city_form_has_placeholder(self):
        '''тест: поле ввода имеет атрибут placeholder'''
        form = CityForm()
        self.assertIn('placeholder="Введите город"', form.as_p())

    def test_form_validation_for_blank_items(self):
        '''тест валидации формы для пустых элементов'''
        form = CityForm(data={'name': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [EMPTY_CITY_ERROR])
