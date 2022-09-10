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


class NewVisitorTest(StaticLiveServerTestCase):
    '''тест нового посетителя'''

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

    def test_can_get_weather_for_cities(self):
        '''тест: можно получить погоду в городах'''
        # Пользователь услышал про новое онлайн приложение
        # где можно узнать текущую погоду в городах мира. Он
        # решает оценить его домашнюю страницу.
        self.browser.get(self.live_server_url)

        # Он видит, что заголовок и шапка страницы говорит о том,
        # что это погодное приложение
        self.assertIn('Погодное приложение', self.browser.title)
        header_text = self.browser.find_element(by=By.TAG_NAME, value='h1').text
        self.assertEqual('Погода в вашем городе', header_text)

        # Пользователю сразу же предлагается узнать погоду в
        # конкретном городе
        inputbox = self.browser.find_element(by=By.ID, value='id_new_city')
        self.assertEqual(inputbox.get_attribute('placeholder'), "Введите город")

        # Пользователь набирает в текстовом поле "Москва" (в этом городе
        # он проживает)
        inputbox.send_keys('Москва')

        # Когда он нажимает кнопку "Узнать", страница обновляется,
        # и теперь страница содержит данные о погоде в Москве.
        # Есть данные о температуре, атмосферном давлении, влажности, ветре,
        # а также есть информативная картинка
        button_to_learn = self.browser.find_element(by=By.ID,
                                                    value='id_to_learn').click()

        self.wait_for_row_in_list_table('Москва')
        self.wait_for_row_in_list_table('Температура')
        self.wait_for_row_in_list_table('Атмосферное давление')
        self.wait_for_row_in_list_table('Влажность')
        self.wait_for_row_in_list_table('Ветер')
        #self.wait_for_row_in_list_table('https://openweathermap.org/img/')

        # Текстовое поле по-прежнему приглашает узнать погоду в городе.
        inputbox = self.browser.find_element(by=By.ID, value='id_new_city')
        self.assertEqual(inputbox.get_attribute('placeholder'), "Введите город")

        # Пользователь набирает в текстовом поле "Сочи" (видимо пользователь
        # хочет перебраться жить в более теплое место)
        inputbox.send_keys('Сочи')

        # Когда он нажимает "Узнать", страница снова обновляется, и теперь
        # показывает данные о погоде в "Сочи",
        # а данные о погоде в "Москва" пропадают.
        button_to_learn = self.browser.find_element(by=By.ID,
                                                    value='id_to_learn').click()
        self.wait_for_row_in_list_table('Сочи')
        self.wait_for_row_in_list_table('Температура')
        self.wait_for_row_in_list_table('Атмосферное давление')
        self.wait_for_row_in_list_table('Влажность')
        self.wait_for_row_in_list_table('Ветер')
        # self.wait_for_row_in_list_table('https://openweathermap.org/img/')

        page_text = self.browser.find_element(by=By.TAG_NAME, value='body').text
        self.assertNotIn('Москва', page_text)

        # Удовлетворённый пользователь ложится спать.