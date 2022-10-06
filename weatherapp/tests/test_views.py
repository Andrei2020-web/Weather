from django.test import TestCase
from django.urls import resolve
from weatherapp.views import home_page, NON_EXISTENT_CITY_ERROR
from django.contrib.auth import get_user_model
from weatherapp.models import City
from weatherapp.forms import CityForm, DUPLICATE_CITY_ERROR
from django.utils.html import escape

User = get_user_model()


class HomePageTest(TestCase):
    '''тест домашней страницы'''

    def test_root_url_resolves_to_home_page_view(self):
        '''тест: корневой url преобразуется в представление
            домашней страницы'''
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        '''тест: используется домашний шаблон'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'weatherapp/home.html')

    def test_can_save_a_POST_request(self):
        '''тест: можно сохранить post-запрос'''

        response = self.client.post('/', data={'name': "Москва"})
        self.assertIn('Москва', response.content.decode())
        self.assertTemplateUsed(response, 'weatherapp/home.html')

    def test_home_page_uses_city_form(self):
        '''тест: домашняя страница использует форму для города'''
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], CityForm)

    def test_unauthorized_user_sees_only_the_last_POST_request(self):
        '''Неавторизованный пользователь видит только последний POST запрос'''

        response1 = self.client.post('/', data={'name': "Москва"})
        response2 = self.client.post('/', data={'name': "Сочи"})

        self.assertIn('Москва', response1.content.decode())
        self.assertTemplateUsed(response1, 'weatherapp/home.html')
        self.assertNotIn('Москва', response2.content.decode())
        self.assertTemplateUsed(response2, 'weatherapp/home.html')

    def test_authorized_user_see_only_all_his_POST_requests(self):
        '''Aвторизованный пользователь видит только все свои POST запросы'''

        user1 = User.objects.create(username='WeatherUser1',
                                    password='%%%%%%%%')
        self.client.force_login(user1)

        response1 = self.client.post('/', data={'name': "Самара"})
        response2 = self.client.post('/', data={'name': "Адлер"})

        self.assertIn('Самара', response1.content.decode())
        self.assertTemplateUsed(response1, 'weatherapp/home.html')
        self.assertIn('Адлер', response2.content.decode())
        self.assertIn('Самара', response2.content.decode())
        self.assertTemplateUsed(response2, 'weatherapp/home.html')
        self.client.logout()

        user2 = User.objects.create(username='WeatherUser2',
                                    password='%%%%%%%%')
        self.client.force_login(user2)
        response1 = self.client.post('/', data={'name': "Москва"})
        response2 = self.client.post('/', data={'name': "Сочи"})

        self.assertIn('Москва', response1.content.decode())
        self.assertNotIn('Самара', response1.content.decode())
        self.assertNotIn('Адлер', response1.content.decode())
        self.assertTemplateUsed(response1, 'weatherapp/home.html')
        self.assertIn('Сочи', response2.content.decode())
        self.assertIn('Москва', response2.content.decode())
        self.assertNotIn('Самара', response2.content.decode())
        self.assertNotIn('Адлер', response2.content.decode())
        self.assertTemplateUsed(response2, 'weatherapp/home.html')

    def test_for_invalid_input_nothing_saved_to_db_for_authorized_user(self):
        '''тест на недопустимый ввод: ничего не сохраняется в бд для
        зарегистрированного пользователя'''
        user1 = User.objects.create(username='WeatherUser1',
                                    password='%%%%%%%%')
        self.client.force_login(user1)
        self.client.post('/', data={'name': ""})
        self.assertEqual(City.objects.count(), 0)

    def test_for_invalid_input_passes_form_to_template(self):
        '''тест на недопустимый ввод: форма передаётся в шаблон'''
        response = self.client.post('/', data={'name': ""})
        self.assertIsInstance(response.context['form'], CityForm)

    def test_duplicate_city_validation_errors_end_up_on_home_page_(self):
        '''тест: ошибки валидации повторяющегося города
            оканчиваются на домашней странице'''
        user1 = User.objects.create(username='WeatherUser1',
                                    password='%%%%%%%%')
        self.client.force_login(user1)
        city1 = City.objects.create(name='Москва', owner=user1)
        response = self.client.post('/', data={'name': 'Москва'})

        expected_error = escape(DUPLICATE_CITY_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'weatherapp/home.html')
        self.assertEqual(City.objects.all().count(), 1)

    def test_non_existent_city_validation_errors_end_up_on_home_page(self):
        '''тест: ошибки валидации несуществующего города
         оканчиваются на домашней странице'''
        user1 = User.objects.create(username='WeatherUser1',
                                    password='%%%%%%%%')
        self.client.force_login(user1)
        response = self.client.post('/', data={'name': 'Которого нет'})
        expected_error = escape(NON_EXISTENT_CITY_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'weatherapp/home.html')
        self.assertEqual(City.objects.all().count(), 0)