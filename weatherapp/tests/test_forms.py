from django.test import TestCase
from weatherapp.forms import CityForm, EMPTY_CITY_ERROR, DUPLICATE_CITY_ERROR
from weatherapp.models import City
from django.contrib.auth import get_user_model

User = get_user_model()

class CityFormTest(TestCase):
    '''тест формы для города'''

    def test_city_form_has_placeholder(self):
        '''тест: поле ввода имеет атрибут placeholder'''
        form = CityForm()
        self.assertIn('placeholder="Введите город"', form.as_p())

    def test_form_validation_for_blank_cities(self):
        '''тест валидации формы для пустых городов'''
        form = CityForm(data={'name': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [EMPTY_CITY_ERROR])

    def test_form_validation_for_duplicate_cities(self):
        '''тест: валидации формы для повторяющихся городов'''
        user1 = User.objects.create(username='WeatherUser1',
                                    password='%%%%%%%%')
        self.client.force_login(user1)
        city = City.objects.create(name='Москва', owner=user1)
        form = CityForm(data={'name': 'Москва'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [DUPLICATE_CITY_ERROR])
