from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, \
    HASH_SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings
import os
import time

MAX_WAIT = 10
User = get_user_model()


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


class FunctionalTest(StaticLiveServerTestCase):
    '''функциональный тест'''

    def setUp(self):
        '''установка'''
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server

    def tearDown(self):
        '''демонтаж'''
        self.browser.quit()

    def get_table_row(self):
        '''получить строки таблицы'''
        return self.browser.find_elements(by=By.CSS_SELECTOR,
                                          value='#id_info_table')

    @wait
    def wait_for_row_in_list_table(self, item_text):
        rows = self.get_table_row()
        for row in rows:
            self.assertIn(item_text, row.text)

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

    def create_pre_authenticated_sessions(self, username, password):
        '''создать предварительно аутентифицированный сеанс'''
        user = User.objects.create(username=username, password=password)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()
        ## установить cookie, которые нужны для первого посещения домена.
        ## страницы 404 загружаются быстрее всего!
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/'
        ))

    def get_item_input_box(self):
        '''получить поле ввода для элемента'''
        return self.browser.find_element(by=By.ID, value='id_new_city')

    def get_item_button(self):
        '''получить кнопку'''
        return self.browser.find_element(by=By.ID, value="id_to_learn")
