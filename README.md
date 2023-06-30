# Проект News
![Github actions](https://github.com/Xanssun/test_task/actions/workflows/main.yml/badge.svg)

- запуск прокета

1. склонируйте репорзиторий.

2. перейдите в папку cd infra.

3. создайте файл .env, согласно шаблону:

- DB_ENGINE=django.db.backends.postgresql
- DB_NAME=postgres
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=postgres
- DB_HOST=db
- DB_PORT=5432

3. команда docker-compose up разверните проект.

4. Сделайте миграции, суперпользователя и соберите статику:

- docker-compose exec web python manage.py migrate
- docker-compose exec web python manage.py createsuperuser
- docker-compose exec web python manage.py collectstatic --no-input

5. Зайдите на (http://127.0.0.1/admin/) и убедитесь, что все работает

# Проект на сервере
- проект досутупен http://158.160.9.119/admin/
- login xans
- password 12345

- http://158.160.9.119/api/users/ - создание пользователей POST
```
{
    "username": "user",
    "password": "ASD123ASD",
    "email": "user@ma.ru"
}

```
- http://158.160.9.119/api/auth/login/ - авторизация POST
```
{
    "username": "user_user",
    "password": "ASD123ASD"
}

```
- http://158.160.9.119/api/news/ - создание новости POST (при запросе GET - получение всех новостей)
```
{
    "date": "2023-06-29",
    "title": "новости1",
    "text": "первые новости",
    "author": "user_user"
}

```
- http://158.160.9.119/api/news/1/comments/ - создание коментария POST
```
{
    "date": "2023-06-29",
    "text": "очень хорошая новость2 от user_user2"
}

```
- http://158.160.9.119/api/news/2/like/ - создание лайка POST (при повторной отправки POST запроса удаляет лайк)

- http://158.160.9.119/api/news/1/comments/2/ - удаление коментария DELETE (нельзя удалить чужой коментарий, если ты не админ)
```
{
    "detail": "You do not have permission to perform this action."
}

```
