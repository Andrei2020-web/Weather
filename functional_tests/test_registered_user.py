from .base import FunctionalTest
from selenium.webdriver.common.by import By


class RegisteredUserTest(FunctionalTest):
    '''тест зарегистрированного пользователя'''

    def test_logged_in_user_cities_can_save(self):
        '''тест: города зарегистрированного пользователя сохраняется'''
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out('WeatherUser1')

        # Пользователь является зарегистрированным пользователем
        self.create_pre_authenticated_sessions('WeatherUser1', '%%%%%%%%')
        self.browser.refresh()
        # Пользователь впервые открывает домашнюю страницу как
        # зарегистрированный пользователь
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in('WeatherUser1')

        # Пользователю предлагается узнать погоду в
        # конкретном городе
        inputbox = self.browser.find_element(by=By.ID, value='id_new_city')
        self.assertEqual(inputbox.get_attribute('placeholder'), "Введите город")

        # Пользователь набирает в текстовом поле "Москва" (в этом городе
        # он проживает)
        inputbox.send_keys('Москва')

        # Когда он нажимает кнопку "Узнать", страница обновляется,
        # и теперь страница содержит данные о погоде в Москве.
        button_to_learn = self.browser.find_element(by=By.ID,
                                                    value='id_to_learn').click()

        self.wait_for_row_in_list_table('Москва')
        self.wait_for_row_in_list_table('Температура')
        self.wait_for_row_in_list_table('Атмосферное давление')
        self.wait_for_row_in_list_table('Влажность')
        self.wait_for_row_in_list_table('Ветер')

        # Текстовое поле по-прежнему приглашает узнать погоду в городе.
        inputbox = self.browser.find_element(by=By.ID, value='id_new_city')
        inputbox.clear()
        self.assertEqual(inputbox.get_attribute('placeholder'), "Введите город")

        # Пользователь набирает в текстовом поле "Сочи" (видимо пользователь
        # хочет перебраться жить в более теплое место)
        inputbox.send_keys('Сочи')

        # Когда он нажимает "Узнать", страница снова обновляется, и теперь
        # показывает данные о погоде в "Сочи" и в "Москва"
        # Данные о погоде в "Москва" не пропадают.
        button_to_learn = self.browser.find_element(by=By.ID,
                                                    value='id_to_learn').click()
        self.wait_for_row_in_list_table('Сочи')
        self.wait_for_row_in_list_table('Москва')

        # Пользователь нажимает на раздел "Главная",
        # обновлённые данные о погоде в городе
        # "Москва" и "Сочи" опять показаны пользователю
        self.browser.find_element(by=By.LINK_TEXT,
                                  value='Главная').click()
        self.wait_for_row_in_list_table('Сочи')
        self.wait_for_row_in_list_table('Москва')

        # Пользователь выходит из системы, нажимает на раздел "Главная".
        # данные о погоде пропадают.
        self.browser.find_element(by=By.LINK_TEXT,
                                  value='Выйти').click()
        self.wait_to_be_logged_out('WeatherUser1')
        self.browser.find_element(by=By.LINK_TEXT,
                                  value='Главная').click()
        page_text = self.wait_for(
            lambda: self.browser.find_element(by=By.TAG_NAME,
                                              value='body').text)
        self.assertNotIn('Москва', page_text)
        self.assertNotIn('Сочи', page_text)

    def test_logged_in_user_cities_can_delete(self):
        '''тест: города зарегистрированного пользователя удаляются'''
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out('WeatherUser1')

        # Пользователь является зарегистрированным пользователем

        # Пользователь открывает домашнюю страницу как
        # зарегистрированный пользователь

        # Пользователю предлагается узнать погоду в
        # конкретном городе

        # Пользователь набирает в текстовом поле "Москва"

        # Когда он нажимает кнопку "Узнать", страница обновляется,
        # и теперь страница содержит данные о погоде в Москве.

        # Текстовое поле по-прежнему приглашает узнать погоду в городе.

        # Пользователь набирает в текстовом поле "Сочи"

        # Когда он нажимает "Узнать", страница снова обновляется, и теперь
        # показывает данные о погоде в "Сочи" и в "Москва"

        # Далее пользователь замечает ссылку "Удалить"
        # над данными о погоде для городов "Москва" и "Сочи"

        # Пользователь нажимает на ссылку "Удалить" для города "Москва"

        # Страница обновляется, и теперь показывает только данные о погоде
        # в "Сочи" данные о погоде в "Москва" пропадают

        # Пользователь ещё раз нажимает на ссылку "Удалить",
        # но уже для города "Сочи"

        # Страница обновляется, данные о погоде в "Сочи" пропадают
