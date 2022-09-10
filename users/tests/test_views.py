from django.test import TestCase
from django.urls import resolve
from users.views import register
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegistrationPageTest(TestCase):
    '''тест страницы регистрации'''

    def test_registration_url_resolves_to_registration_view(self):
        '''тест: регистрационный url преобразуется в представление
        страницы регистрации'''

        found = resolve('/users/register/')
        self.assertEqual(found.func, register)

    def test_registration_page_returns_correct_html(self):
        '''тест: используется шаблон регистрации'''

        response = self.client.get('/users/register/')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_registration_page_uses_registration_form(self):
        '''тест: страница регистрации использует форму для регистрации'''
        response = self.client.get('/users/register/')
        self.assertIsInstance(response.context['form'], UserCreationForm)

    def test_post_request_can_register_a_new_user(self):
        '''post-запрос может зарегистрировать нового пользователя'''

        response = self.client.post('/users/register/', data={'username': "WeatherUser1",
                                                              'password1': "%%%%%%%%",
                                                              'password2': "%%%%%%%%",
                                                              })
        newUser = User.objects.get(username='WeatherUser1')
        self.assertEqual(newUser.username, 'WeatherUser1')
        self.assertRedirects(response, '/')
