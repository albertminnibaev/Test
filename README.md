# Сервис для реферальной системы
1. Перед началом работы в корне проекта необходимо создать файл .env для хранения переменных окружения.
Файл .env создается на основе файла .env.sample.
Файл .env содержит следующие переменные:
   * SECRET_KEY - секретный ключ Django;
   * PASSWORD_DATABASE - пароль для подключения к базе данных;
   * API_KEY - сукретный ключ для проверки указанного email адреса через сайт emailhunter.co (для получения необходимо зарегистрироваться на сайте emailhunter.co);
   * CACHE_ENABLED - переменная для включения или отключения кешиования (1 - включено, 0 - отключено);
   * CACHE_LOCATION -  адрес брокера (redis://127.0.0.1:6379) 

2. Для кеширования используется REDIS
3. Для регистрации и аутентификации используется стандартные инструменты Django REST framework с использованием библиотеку djangorestframework-simplejwt
4. Для запуска проекта необходимо запустить Redis командой - sudo service redis-server start, и запустить само приложение коммандой - python manage.py runserver

## Описание документации к API:
Для автоматической регистрации используются Swagger и Redoc.
Пример основных запросов:
1. Регистрация пользователя:


    запрос POST user/register/
    параметры запроса
    {
      "email": "user@example.com",
      "password": "string",
      "first_name": "string",
      "last_name": "string"
    }

    ответ: 

    статус код: 201 OK

    {
      "email": "user@example.com",
      "password": "string",
      "first_name": "string",
      "last_name": "string"
    }

2. Регистрация пользователя как реферала:


    запрос POST user/register_referral/
    параметры запроса
    {
      "email": "user@example.com",
      "password": "string",
      "first_name": "string",
      "last_name": "string",
      "referral_code_refer": "string"
    }

    ответ: 

    статус код: 201 OK

    {
      "email": "user@example.com",
      "password": "string",
      "first_name": "string",
      "last_name": "string",
      "referral_code_refer": "string"
    }

3. Получение информации о рефералах по id рефера:


    запрос GET user/referral/{id}/

    ответ: 

    статус код: 200 OK

    {
        "referral": [
           {
               "id": 0,
               "password": "string",
               "last_login": "2019-08-24T14:15:22Z",
               "is_superuser": true,
               "is_staff": true,
               "is_active": true,
               "date_joined": "2019-08-24T14:15:22Z",
               "first_name": "string",
               "last_name": "string",
               "email": "user@example.com",
               "image": "http://example.com",
               "referral_code_refer": "string",
               "referral": 0,
               "groups": [],
               "user_permissions": []
           }
        ]
    }

4. Создание реферального ключа:


    запрос POST code/create/
    параметры запроса
    {}

    ответ: 

    статус код: 201 OK

    {}

5. Создание реферального ключа:


    запрос POST code/delete/
    параметры запроса
    {}

    ответ: 

    статус код: 204_NO_CONTENT

    {}

6. Получение реферального ключа по email адресу реферра:


    запрос POST code/delete/
    параметры запроса
    {
        "email": "user@example.com"
    }

    ответ: 

    статус код: 200

    {
        "referral_code": "191850"
    }
