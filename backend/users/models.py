from core.help_text import (help_max_len_email, help_txt_first_last_name,
                            help_txt_username)
from django.contrib.auth.models import AbstractUser
from django.db import models

SLUG_LEN = 50
EMAIL_LEN = 256
USER_LEN = 150


class User(AbstractUser):
    """Кастомная модель для юзера"""

    username = models.CharField('Уникальное имя пользователя',
                                max_length=USER_LEN,
                                unique=True, blank=False, null=False,
                                help_text=help_txt_username)
    email = models.EmailField('Электронная почта', max_length=EMAIL_LEN,
                              unique=True, blank=False, null=False,
                              help_text=help_max_len_email)
    first_name = models.CharField('Имя', max_length=USER_LEN, blank=False,
                                  null=False,
                                  help_text=help_txt_first_last_name)
    last_name = models.CharField('Фамилия', max_length=USER_LEN,
                                 blank=False, null=False,
                                 help_text=help_txt_first_last_name)
    password = models.CharField(
        'Пароль', max_length=USER_LEN,
        help_text=help_txt_first_last_name,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email',
                violation_error_message=(
                    'Пользователь с таким именем или email существует')
            )
        ]

    @property
    def is_admin(self):
        return self.is_superuser

    def __str__(self):
        return f'{self.username}, {self.email}, {self.first_name}'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow',
                violation_error_message='Вы уже подписаны на этого автора'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на  {self.author}'
