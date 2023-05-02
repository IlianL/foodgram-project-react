## Продуктовый помощник
![workflow](https://github.com/IlianL/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)  

## Tech stack:
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Djoiser](https://img.shields.io/badge/-djoiser-%23008080?style=for-the-badge&logo=appveyor)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)  

![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)  

![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)  

![Yandex.cloud](https://img.shields.io/badge/-yandex.clound-blue?style=for-the-badge&logo=appveyor)  

***
Привет! Если проект оказался полезен буду признателен за звездочку [репозиторию](https://github.com/IlianL/foodgram-project-react.git).  
Если есть вопросы мой тг в профиле, всегда рад помочь.
***

## Описание
Cервис для публикаций и обмена рецептами.

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Запуск проекта на сервере.
Скачайте проект
 ```
# Нам нужна только папка infra
https://github.com/IlianL/foodgram-project-react.git
 ```
Подключитесь к своему серверу
```
ssh your_login@your_ip
```
Обновляем список пакетов и обновляем сами пакеты.
```
sudo apt update
sudo apt upgrade -y 
```
Устанавливаем докер и докер компоуз.
```
sudo apt install docker.io
sudo apt install docker-compose
# Если у вас не ubuntu, воспользуйтесь этой инструкцией для установки docker-compose:
# https://docs.docker.com/compose/install/
```
Проверяем успешность установки.
```
docker --version
docker-compose --version
```
Создайте на сервере директорию для проекта.
```
mkdir foodgram && cd foodgram/
```
Создайте и заполните .env файл по примеру.
```
nano .env
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=example_pwd # пароль для подключения к БД
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY=shhh_secret # секретный ключ джанго
DEBUG=False
```
Отредактируйте файл infra/nginx.conf.
```
# Замените этот адрес на адрес вашего сервера.
server_name 127.0.0.1;
```
Скопируйте файлы из папки infra на ваш сервер.
```
# В момент выполнения команды нужно находиться в корневой папке проекта
# D:/.../foodgram-project-react/
scp -r infra/*  <username>@<server IP>:/home/<server user>/foodgram/
```
Запустите контейнеры.
```
sudo docker-compose up -d
```
После успешной сборки выполнить эти команды:
```
# Делаем миграции.
sudo docker-compose exec -T backend python manage.py makemigrations
sudo docker-compose exec -T backend python manage.py migrate
# Импортируем в БД ингредиенты и тэги.
sudo docker-compose exec backend python manage.py importcsv
# Собирем статику.
sudo docker-compose exec -T backend python manage.py collectstatic --no-input
# Создаём администратора.
sudo docker-compose exec backend python manage.py createsuperuser
```
Теперь проект доступен по адресу вашего сервера.
```
# Документация доступна по адресу:
http://[ваш сервер]/api/docs/  
# Админ зона:
http://[ваш сервер]/admin/
```

Остановка и повторный запуск проекта.
```
# Отсанавлием контейнеры без удаления.
sudo docker-compose stop
# Запускаем остановленные контейнеры.
sudo docker-compose start
# Останавливаем и удаляем контейнеры, ключ -v удаляет тома.
sudo docker-compose down -v
```
  
Автор: Илиан Ляпота
