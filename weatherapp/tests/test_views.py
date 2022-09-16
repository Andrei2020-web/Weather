from django.test import TestCase
from django.urls import resolve
from weatherapp.views import home_page
from django.contrib.auth import get_user_model

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
