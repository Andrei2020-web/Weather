from selenium.webdriver.common.by import By
from .base import FunctionalTest


class CityValidation(FunctionalTest):
    '''тест валидации города'''

    def get_error_element(self):
        '''получить элемент с ошибкой'''
        return self.browser.find_element(by=By.CSS_SELECTOR, value='.has-error')

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

    def test_registered_user_cannot_add_duplicate_info_on_page(self):
        '''тест: зарегистрированный пользователь не может добавить повторяющуюся
         информацию на страницу'''
        # Зарегистрированный пользователь открывает домашнюю страницу
        # и вводит в текстовом поле "Москва"
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out('WeatherUser1')
        self.create_pre_authenticated_sessions('WeatherUser1', '%%%%%%%%')
        self.browser.refresh()
        self.get_item_input_box().send_keys('Москва')

        # Когда он нажимает кнопку "Узнать", страница обновляется,
        # и теперь страница содержит данные о погоде в Москве.
        self.get_item_button().click()
        self.wait_for_row_in_list_table('Москва')

        # Пользователь случайно ещё раз вводит город "Москва"
        self.get_item_input_box().clear()
        self.get_item_input_box().send_keys('Москва')
        self.get_item_button().click()

        # Он видит полезное сообщение об ошибке
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text.replace('* ', ''),
            "Вы уже получили информацию по данному городу."
        ))

    def test_cannot_find_out_weather_in_non_existent_city(self):
        '''тест: нельзя узнать погоду в несуществующем городе'''
        # Пользователь открывает домашнюю страницу и вводит
        # в текстовом поле "Которого нет"

        # Когда он нажимает кнопку "Узнать", страница обновляется,
        # и теперь он видит полезное сообщение об ошибке
