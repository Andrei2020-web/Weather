from django.test import TestCase
from django.contrib.auth import get_user_model
from weatherapp.models import City

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
