from selenium.webdriver.common.by import By

from .base import FunctionalTest


class CityValidation(FunctionalTest):
    '''тест валидации города'''

    def test_cannot_find_out_weather_without_city_name(self):
        '''тест: нельзя узнать погоду не указав название города'''
        # Пользователь открывает домашнюю страницу и случайно пытается узнать
        # погоду не указав название города.
        # Он нажимает кнопку "Узнать" с пустым полем ввода
        self.browser.get(self.live_server_url)
        self.get_item_button().click()

        # Браузер перехватывает запрос и не загружает данные о погоде
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR,
                                                        value='#id_new_city:invalid'))

        # Пользователь начинает набирать название нового города
        # и ошибка исчезает
        self.get_item_input_box().send_keys('Москва')
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR,
                                                        value='#id_new_city:valid'))

        # И он может отправить его успешно
        self.get_item_button().click()
        self.wait_for_row_in_list_table('Москва')

        # Пользователь опять пытается узнать погоду не указав название города
        self.get_item_button().click()

        # И снова браузер не подчиняется
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR,
                                                        value='#id_new_city:invalid'))

        # И он может это исправить, заполнив поле текстом
        self.get_item_input_box().send_keys('Сочи')
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR,
                                                        value='#id_new_city:valid'))
        self.get_item_button().click()
        self.wait_for_row_in_list_table('Сочи')
