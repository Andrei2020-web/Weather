# Weather
___
![python_version](https://img.shields.io/badge/python-3.10-orange)
![django_version](https://img.shields.io/badge/django-4.1-orange)
![selenium_version](https://img.shields.io/badge/selenium-4.4-orange)
![bootstrap_version](https://img.shields.io/badge/bootstrap-5-orange)
![requests_version](https://img.shields.io/badge/requests-2.28-orange)

Онлайн приложение, где можно узнать текущую погоду в городах мира.
В данном приложении можно регистрироваться,
узнавать данные о погоде в городах мира, сохранять их в бд и просматривать в дальнейшем.
![demo](demo.jpg)

## Настройка перед запуском

Первое, что нужно сделать, это cклонировать репозиторий:

```sh
$ git clone https://github.com/Andrei2020-web/Weather.git
$ cd weather
```

Создайте виртуальную среду для установки зависимостей и активируйте ее:

```sh
$ virtualenv venv
$ source venv/bin/activate
```

Затем установите зависимости:

```sh
(venv)$ pip install -r requirements.txt
```

Запускаем сервер:

```sh
(venv)$ python manage.py runserver
```
