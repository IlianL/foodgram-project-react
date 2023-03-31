# Generated by Django 4.1.7 on 2023-03-31 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_subscription_subscription_unique_follow'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='subscription',
            name='unique_follow',
        ),
        migrations.RemoveConstraint(
            model_name='user',
            name='unique_username_email',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text='Обязательное поле. Максимальная длина 256', max_length=256, unique=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(help_text='Обязательное поле. Максимальная длина 150', max_length=150, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(help_text='Обязательное поле. Максимальная длина 150', max_length=150, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(help_text='Обязательное поле. Максимальная длина 150', max_length=150, verbose_name='Пароль'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Обязательное поле. Максимальная длина 150Буквы, цифры и симdолы: . @ + - _', max_length=150, unique=True, verbose_name='Уникальное имя пользователя'),
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_follow', violation_error_message='Вы уже подписаны на этого автора'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('username', 'email'), name='unique_username_email', violation_error_message='Пользователь с таким именем или email существует'),
        ),
    ]
