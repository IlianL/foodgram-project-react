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



***Уф, это было сложно, около 30  коммитов только для отладки workflow да простят меня сервера гит! Я всё проверил, всё должно работать идеально. У меня были проблемы с корзиной (не появлялись рецепты) пока копался с этой проблемой нашёл момент, мы ведь  получаем  рецепт\корзину по пк:***
```
        shopping_cart = set(
            ShoppingCart.objects.filter(
                user_id=self.request.user.idб recipe_id=self.kwargs.get('pk')).values_list(
                    'recipe_id', flat=True)) 
```
***так вот, если сделать гет запрос на весь список рецептов (api\recipes) в кваргс не будет pk, а значит все значения is_favorite and is_in_shopping_cart будут false в любом случае. Я удалил  recipe_id=self.kwargs.get('pk'). теперь в сет закидывает всю корзину\избранное, это гуд?  
На уровне с этим ридми есть воркфлоу, будет здорово если ты его посмотришь <3  
В серилайзерах на сторке 206 мой эксперимент с аннотейтом он в коментах но работает, на твой суд)))  (если совсем стыдно станет, знай, всё это я делал с температурой 38 :DD)  
ПС. скрипты для менеджера это круто, жаль раньше они обошли меня стороной :(***

Сайт - http://158.160.52.113/  
```
admin
login - admin
pwd - gfhjkm111
user_1
email - chief@cook.ru
pwd - gfhjkm111
user_2
email - u2@u.ru
pwd - gfhjkm111
```

## Описание
Cервис для публикаций и обмена рецептами.

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


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
5. Cкопируйте файлы docker-compose.yaml и nginx.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.

6. Запуск  
Команда git push является тригером воркфлоу.
Послу команды пуш нужно зайти на сервер и выполнить эти команды по очереди:
```
sudo docker-compose exec -T backend python manage.py migrate
# Импортируем в БД ингредиенты и тэги.
sudo docker-compose exec backend python manage.py importcsv
sudo docker-compose exec -T backend python manage.py collectstatic --no-input
# Создаём администратора.
sudo docker-compose exec backend python manage.py createsuperuser
```
Теперь проект доступен на по адресу вашего сервера.
