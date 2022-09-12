from .base import FunctionalTest
from selenium.webdriver.common.by import By


class LoginTest(FunctionalTest):
    '''тест регистрации в системе'''

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
