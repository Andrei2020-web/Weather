from django.test import TestCase
from weatherapp.forms import CityForm

class CityFormTest(TestCase):
    '''тест формы для города'''

    def test_city_form_has_placeholder(self):
        '''тест: поле ввода имеет атрибут placeholder'''
        form = CityForm()
        self.assertIn('placeholder="Введите город"', form.as_p())
