from django.test import TestCase
from django.contrib.auth import get_user_model
from weatherapp.models import City
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

User = get_user_model()


class CityModelTest(TestCase):
    '''тест модели города'''

    def test_user_is_related_to_city(self):
        '''тест: пользователь связан с городом'''
        user1 = User.objects.create(username='WeatherUser1',
                                    password='%%%%%%%%')
        user2 = User.objects.create(username='WeatherUser2',
                                    password='%%%%%%%%')
        city1 = City.objects.create(name='Москва', owner=user1)
        city2 = City.objects.create(name='Сочи', owner=user2)
        self.assertIn(city1, user1.city_set.all())
        self.assertIn(city2, user2.city_set.all())

    def test_string_representation(self):
        '''тест строкового представления'''
        city = City(name='Москва')
        self.assertEqual(str(city), 'Москва')

    def test_city_name_is_necessary(self):
        '''тест: название города является обязательным'''
        user1 = User.objects.create(username='WeatherUser1',
                                    password='%%%%%%%%')
        self.client.force_login(user1)
        city = City(name='', owner=user1)
        with self.assertRaises(ValidationError):
            city.save()
            city.full_clean()

    def test_city_owner_is_necessary(self):
        '''тест: владелец города является обязательным'''
        city = City(name='Москва')
        with self.assertRaises(IntegrityError):
            city.save()
            city.full_clean()