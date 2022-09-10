from django.test import TestCase
from django.urls import resolve
from weatherapp.views import home_page


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

        response = self.client.post('/', data={'new_city': "Москва"})
        self.assertIn('Москва', response.content.decode())
        self.assertTemplateUsed(response, 'weatherapp/home.html')


    def test_unauthorized_user_sees_only_the_last_POST_request(self):
        '''Неавторизованный пользователь видит только последний POST запрос'''

        response1 = self.client.post('/', data={'new_city': "Москва"})
        response2 = self.client.post('/', data={'new_city': "Сочи"})

        self.assertIn('Москва', response1.content.decode())
        self.assertTemplateUsed(response1, 'weatherapp/home.html')
        self.assertNotIn('Москва', response2.content.decode())
        self.assertTemplateUsed(response2, 'weatherapp/home.html')
