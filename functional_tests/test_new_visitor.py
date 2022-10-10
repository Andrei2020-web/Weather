from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    '''тест нового посетителя'''

    def test_can_get_weather_for_cities(self):
        '''тест: можно получить погоду в городах'''
        # Пользователь услышал про новое онлайн приложение
        # где можно узнать текущую погоду в городах мира. Он
        # решает оценить его домашнюю страницу.
        self.browser.get(self.live_server_url)

        # Он видит, что заголовок и шапка страницы говорит о том,
        # что это погодное приложение
        self.assertIn('Погодное приложение', self.browser.title)
        header_text = self.get_item_header().text
        self.assertEqual('Погода в вашем городе', header_text)

        # Пользователю сразу же предлагается узнать погоду в
        # конкретном городе
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'), "Введите город")

        # Пользователь набирает в текстовом поле "Москва" (в этом городе
        # он проживает)
        inputbox.send_keys('Москва')

        # Когда он нажимает кнопку "Узнать", страница обновляется,
        # и теперь страница содержит данные о погоде в Москве.
        # Есть данные о температуре, атмосферном давлении, влажности, ветре,
        # а также есть информативная картинка
        self.get_item_button().click()

        self.wait_for_row_in_list_table('Москва')
        self.wait_for_row_in_list_table('Температура')
        self.wait_for_row_in_list_table('Атмосферное давление')
        self.wait_for_row_in_list_table('Влажность')
        self.wait_for_row_in_list_table('Ветер')
        # self.wait_for_row_in_list_table('https://openweathermap.org/img/')

        # Текстовое поле по-прежнему приглашает узнать погоду в городе.
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'), "Введите город")

        # Пользователь набирает в текстовом поле "Сочи" (видимо пользователь
        # хочет перебраться жить в более теплое место)
        inputbox.send_keys('Сочи')

        # Когда он нажимает "Узнать", страница снова обновляется, и теперь
        # показывает данные о погоде в "Сочи",
        # а данные о погоде в "Москва" пропадают.
        self.get_item_button().click()
        self.wait_for_row_in_list_table('Сочи')
        self.wait_for_row_in_list_table('Температура')
        self.wait_for_row_in_list_table('Атмосферное давление')
        self.wait_for_row_in_list_table('Влажность')
        self.wait_for_row_in_list_table('Ветер')
        # self.wait_for_row_in_list_table('https://openweathermap.org/img/')

        page_text = self.get_item_body().text
        self.assertNotIn('Москва', page_text)

        # Удовлетворённый пользователь ложится спать.