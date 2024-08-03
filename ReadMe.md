# Проект интеграции почты

Этот проект является тестовым заданием для COMSOFTLAB и предназначен для интеграции нескольких почтовых аккаунтов в одно веб-приложение с использованием Django и Channels для обновлений в реальном времени.

## Возможности

- Добавление нескольких почтовых аккаунтов (Yandex, Gmail, Mail.ru)
- Получение и отображение писем из добавленных аккаунтов
- Обновление прогресса в реальном времени во время получения и сохранения писем
- Переключение между различными почтовыми аккаунтами

## Используемый стек

- Django
- Django Channels
- WebSockets
- HTML, CSS, JavaScript (jQuery)

## Установка

### Минимальные версии

- Python 3.8+
- Django 4.2+

### Настройка

1. Клонируйте репозиторий:

    ```sh
    git clone https://github.com/yourusername/mail-integration.git
    cd mail-integration
    ```

2. Создайте виртуальное окружение и активируйте его:

    ```sh
    python -m venv venv
    source venv/bin/activate   # В Windows используйте `venv\Scripts\activate`
    ```

3. Установите необходимые пакеты:

    ```sh
    pip install -r requirements.txt
    ```

4. Настройте базу данных:

    ```sh
    python manage.py migrate
    ```

5. Создайте суперпользователя:

    ```sh
    python manage.py createsuperuser
    ```

6. Запустите сервер:

    ```sh
    daphne -p 8000 mail_integration.asgi:application
    ```

## Использование

1. Откройте браузер и перейдите по адресу `http://localhost:8000/`.
2. Добавьте новый почтовый аккаунт, заполнив поля email, пароль и выбрав провайдера.
4. После добавления аккаунта вы будете перенаправлены на страницу списка писем, где сможете увидеть полученные письма.
5. Используйте выпадающий список "Переключить почтовый аккаунт" для переключения между различными почтовыми аккаунтами.
6. Нажмите "Обновить письма", чтобы получить и отобразить последние письма.

## Структура проекта
- mail_integration/
- ├── mails/
- │ ├── migrations/
- │ ├── templates/
- │ │ └── mails/
- │ │ ├── email_list.html
- │ │ ├── index.html
- │ │ └── confirm_update.html
- │ ├── init.py
- │ ├── admin.py
- │ ├── apps.py
- │ ├── consumers.py
- │ ├── forms.py
- │ ├── mail_service.py
- │ ├── models.py
- │ ├── routing.py
- │ ├── urls.py
- │ ├── views.py
- │ └── tests.py
- ├── mail_integration/
- │ ├── init.py
- │ ├── asgi.py
- │ ├── settings.py
- │ ├── urls.py
- │ └── wsgi.py
- ├── manage.py
- └── README.md

## Лицензия

Этот проект лицензирован по лицензии MIT.
