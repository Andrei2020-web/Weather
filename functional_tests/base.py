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
