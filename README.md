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


## Описание
Cервис для публикаций и обмена рецептами.

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Подготовка к запуску проекта на сервере.
Для работы с GitHub Actions необходимо из репозитория перейти в раздел Settings > Secrets and variables > Actions создать переменные окружения:
```
DOCKER_USERNAME            # логин Docker Hub
DOCKER_PASSWORD            # пароль от Docker Hub
VM_HOST                    # публичный IP сервера
VM_USER                    # имя пользователя на сервере
SSH_KEY                    # приватный ssh-ключ
PASSPHRASE                 # *если ssh-ключ защищен паролем
DEBUG                      # False
SECRET_KEY_DJANGO_SETTINGS # секретный ключ Django проекта
TELEGRAM_TO                # ID телеграм-аккаунта, куда будут отправляться сообщения
TELEGRAM_TOKEN             # токен бота, посылающего сообщения

DB_ENGINE                  # django.db.backends.postgresql
DB_NAME                    # postgres
POSTGRES_USER              # postgres
POSTGRES_PASSWORD          # задайте свой пароль для БД
DB_HOST                    # db
DB_PORT                    # 5432 
```
  
Отредактируйте конфигурацию сервера infra/nginx.conf
```
# Заментие данные в строке server_name на адрс вашего сервера
# Пример:
server_name foodgramm.com;
```
  
Cоздайте .env файл по пути foodgram-project-react/backend/.env и заполните его по примеру:
```
DB_ENGINE                  # django.db.backends.postgresql
DB_NAME                    # postgres
POSTGRES_USER              # postgres
POSTGRES_PASSWORD          # задайте свой пароль для БД
DB_HOST                    # db
DB_PORT                    # 5432
DEBUG                      # False
SECRET_KEY                 # секретный ключ Django проекта
```

## Деплой:

1. Подключитесь к своему серверу
```
ssh your_login@your_ip
```
2. Обновляем список пакетов и обновляем сами пакеты.
```
sudo apt update
sudo apt upgrade -y 
```
3. Устанавливаем докер и докер компоуз.
```
sudo apt install docker.io
sudp apt install docker-compose
```
4. Проверяем успешность установки.
```
docker --version
docker-compose -- version
```
5. Cкопируйте файлы docker-compose.yaml и nginx.conf из проекта на сервер в home/username/docker-compose.yaml и home/username/nginx.conf соответственно.
```
# Выполните команду находясь в папке infra
scp docker-compose.yml nginx.conf <username>@<host>:/home/<username>/ 
```
6. Создать и запустить контейнеры Docker.
```
# На сервера находясь в директории /home/<username>/
docker-compose up -d
```
7. Workflow. Команда git push является тригером воркфлоу, при этом происходит:
- Проверка кода на соответствие стандарту PEP8
- Сборка и доставка докер-образов frontend и backend на Docker Hub
- Остановка и удаление страых контейнеров на сервере. 
- Разворачивание проекта на удаленном сервере
- Отправка сообщения в Telegram в случае успеха
  
8. После успешной сборки выполнить эти команды:
```
# Делаем миграции.
sudo docker-compose exec -T backend python manage.py migrate
# Импортируем в БД ингредиенты и тэги.
sudo docker-compose exec backend python manage.py importcsv
# Собирем статику.
sudo docker-compose exec -T backend python manage.py collectstatic --no-input
# Создаём администратора.
sudo docker-compose exec backend python manage.py createsuperuser
```
  
9. Остановка и повторный запуск проекта.
```
# Отсанавлием контейнеры без удаления.
sudo docker-compose stop
# Запускаем остановленные контейнеры.
sudo docker-compose start
# Останавливаем контейнеры и удаляем, ключ -v удаляет тома.
sudo docker-compose down -v
```


  
Теперь проект доступен по адресу вашего сервера.
```
# Документация доступна по адресу:
http://[ваш сервер]/api/docs/  
# Админ зона:
http://[ваш сервер]/admin/
```
  
Автор: Илиан Ляпота
