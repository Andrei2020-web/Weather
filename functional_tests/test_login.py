from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import os
import time

MAX_WAIT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    return modified_fn


class LoginTest(StaticLiveServerTestCase):
    '''тест регистрации в системе'''

    def setUp(self):
        '''установка'''
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server

    def tearDown(self):
        '''демонтаж'''
        self.browser.quit()

    @wait
    def wait_for(self, fn):
        '''ожидать'''
        return fn()

    @wait
    def wait_to_be_logged_in(self, username):
        '''ожидать входа в систему'''
        self.browser.find_element(by=By.LINK_TEXT, value='Выйти')
        navbar = self.browser.find_element(by=By.CSS_SELECTOR, value='.navbar')
        self.assertIn(username, navbar.text)

    @wait
    def wait_to_be_logged_out(self, username):
        '''ожидать выхода из системы'''
        self.browser.find_element(by=By.LINK_TEXT, value='Войти')
        navbar = self.browser.find_element(by=By.CSS_SELECTOR, value='.navbar')
        self.assertNotIn(username, navbar.text)

    def test_can_register(self):
        '''тест: можно зарегистрироваться в системе'''

        # Пользователь заходит на сайт и впервые замечает раздел "Регистрация"
        # в навигационной панели. Пользователь нажимает на данный раздел
        self.browser.get(self.live_server_url)
        self.browser.find_element(by=By.LINK_TEXT,
                                  value='Регистрация').click()

        # Страница перезагружается и перед пользователем представлена форма регистрации
        # нового пользователя в которой он должен указать "логин\пароль"

        header_text = self.wait_for(
            lambda: self.browser.find_element(by=By.TAG_NAME, value='h1').text
        )
        self.assertEqual('Зарегистрируйте свой аккаунт', header_text)

        # Пользователь указывает "логин\пароль" и нажимает кнопку регистрации
        inputbox = self.browser.find_element(by=By.ID, value='id_username')
        inputbox.send_keys('WeatherUser1')

        inputbox = self.browser.find_element(by=By.ID, value='id_password1')
        inputbox.send_keys('%%%%%%%%')

        inputbox = self.browser.find_element(by=By.ID, value='id_password2')
        inputbox.send_keys('%%%%%%%%')

        self.browser.find_element(by=By.ID, value='id_register').click()

        # Теперь пользователь зарегистрирован в системе
        self.wait_to_be_logged_in('WeatherUser1')

        # Теперь пользователь замечает раздел "Выйти" и
        # нажимает на этот раздел
        self.browser.find_element(by=By.LINK_TEXT,
                                  value='Выйти').click()

        # Страница перезагружается и теперь пользователь стал
        # обычным пользователем
        self.wait_to_be_logged_out('WeatherUser1')

        # Теперь пользователь замечает раздел "Войти" в навигационной панели.
        # Пользователь нажимает на данный раздел
        self.browser.find_element(by=By.LINK_TEXT,
                                  value='Войти').click()

        # Страница перезагружается и перед пользователем представлена форма
        # входа в которой он должен указать "логин\пароль"
        header_text = self.wait_for(
            lambda: self.browser.find_element(by=By.TAG_NAME, value='h1').text
        )
        self.assertEqual('Войдите в свой аккаунт', header_text)

        # Пользователь указывает "логин\пароль" и нажимает кнопку "Войти"
        inputbox = self.browser.find_element(by=By.ID, value='id_username')
        inputbox.send_keys('WeatherUser1')

        inputbox = self.browser.find_element(by=By.ID, value='id_password')
        inputbox.send_keys('%%%%%%%%')

        self.browser.find_element(by=By.ID, value='id_login').click()

        # Теперь пользователь зарегистрирован в системе
        self.wait_to_be_logged_in('WeatherUser1')
