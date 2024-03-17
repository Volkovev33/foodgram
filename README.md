# Проект Foodgram
![example workflow](https://github.com/Volkovev33/foodgram-project-react/actions/workflows/main.yml/badge.svg)  
  
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
![Swagger Validator](https://img.shields.io/swagger/valid/3.0?specUrl=https%3A%2F%2Fraw.githubusercontent.com%2FOAI%2FOpenAPI-Specification%2Fmaster%2Fexamples%2Fv2.0%2Fjson%2Fpetstore-expanded.json)



Лучший проект для фоток еды и публикации рецептов.

## Подготовка и запуск проекта
### Склонировать репозиторий на локальную машину:
## Для работы с удаленным сервером (на ubuntu):
* Выполните вход на свой удаленный сервер

* Установите docker на сервер:
```
sudo apt install docker.io 
```
* Установите docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```  
* Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

* Cоздайте .env файл и впишите:
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    SECRET_KEY=<секретный ключ проекта django>
    DEBUG=<статус дебага>
    ALLOWED_HOSTS=<список разрешённых хостов>
    CSRF_TRUSTED_ORIGINS=<fqdn хоста>
    ```
* Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    
    DOCKER_PASSWORD=<пароль от DockerHub>
    DOCKER_USERNAME=<имя пользователя>
    
    SECRET_KEY=<секретный ключ проекта django>

    USER=<username для подключения к серверу>
    HOST=<IP сервера>
    PASSPHRASE=<пароль для сервера, если он установлен>
    SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>
    
    DEBUG=<статус дебага>
    ALLOWED_HOSTS=<список разрешённых хостов>
    ```
    Workflow состоит из двух шагов:
     - Сборка и публикация образа бекенда на DockerHub.
     - Автоматический деплой на удаленный сервер.

* На сервере соберите docker-compose:
```
sudo docker compose up -d --build
```
* После успешной сборки на сервере выполните команды (только после первого деплоя):
    - Соберите статические файлы:
    ```
    sudo docker compose exec backend python manage.py collectstatic --noinput
    ```
    - Примените миграции:
    ```
    sudo docker compose exec backend python manage.py makemigrations
    sudo docker compose exec backend python manage.py migrate --noinput
    ```
    - Загрузите ингридиенты  в базу данных (необязательно):  
    *По умолчанию выберется ingredients.json*
    ```
    sudo docker compose exec backend python manage.py load_ingredients <Название файла из директории data>
    ```
    - Создать суперпользователя Django:
    ```
    sudo docker compose exec backend python manage.py createsuperuser
    ```
    - Проект будет доступен по вашему IP

## Доступные эдпоинты
При после запуска, список доступных запросов, можно увидеть в документации к апи:
(реализована автодокументация с использованием swagger)
```
<adpress>/api/docs/
```

## Проект в интернете
Проект запущен и доступен по [адресу](https://yaprojects.ddns.net/)

### Основные эндпоинты
Документация:
```
http://yaprojects.ddns.net/api/api/docs/
```
Ингридиенты:
```
http://yaprojects.ddns.net/api/ingredients/
```
Рецепты:
```
https://yaprojects.ddns.net/api/recipes/
```
Теги:
```
http://yaprojects.ddns.net/api/tags/
```
Пользователи:
```
http://yaprojects.ddns.net/api/users/
```
