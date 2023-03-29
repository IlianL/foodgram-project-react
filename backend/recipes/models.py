from django.core.validators import MinValueValidator
from django.db import models
from users.models import User

MAX_NAME = 200
MAX_HEX = 7


class Tag(models.Model):
    """Модель тэгов."""
    name = models.CharField('Название', max_length=MAX_NAME, unique=True)
    color = models.CharField('Цвет в HEX', max_length=MAX_HEX, unique=True)
    slug = models.SlugField('Уникальный слаг', max_length=MAX_NAME,
                            unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} цвет: {self.color}'


class Ingredient(models.Model):
    """Модель для списка индигриентов."""
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_NAME)
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=MAX_NAME)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги')

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes',
        verbose_name='Автор')

    ingredient = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингредиенты',
        through='AmountIngredientInRecipe'
    )
    name = models.CharField(
        verbose_name='Название блюда',
        max_length=MAX_NAME)
    text = models.TextField('Описание блюда')
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipes/images/',
        null=True,
        default=None)
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        default=0,
        validators=(MinValueValidator(
            1, 'Минимальное время приготовления - одна минута'),
        )
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)
        constraints = (models.UniqueConstraint(
                       fields=('name', 'author'),
                       name='unique_for_author',),
                       )

    def __str__(self):
        return self.name


class AmountIngredientInRecipe(models.Model):
    """
    Связываем модели Recipe и Ingredient, добавляем количество ингредиентов.
    """
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='ingredient_list',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='ingredient_list',
        on_delete=models.CASCADE
    )
    amount = models.SmallIntegerField(
        verbose_name='Количество',
        default=0,
        validators=(MinValueValidator(
            1, 'Минимальное количество ингредиентов - один'),
        )
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ('id',)
        constraints = (models.UniqueConstraint(
                       fields=('recipe', 'ingredient'),
                       name='unique_recipe_ingredient',
                       ),)

    def __str__(self):
        return (f'{self.ingredient.name} ({self.ingredient.measurement_unit})'
                f' - {self.amount}')


class Favorite(models.Model):
    """Модель для избраного."""
    # Для Favorite и  ShoppingCart можно было бы сделать абстрактную модель
    # но риэйтед нейм формата "%(app_label)s_%(class)s_related",
    # не очень, с учётом того что verbose_name ещё переписывать
    # мне кжается не стоит оно того.
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorite_list'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Понравившейся рецепт',
        on_delete=models.CASCADE,
        related_name='favorite_list'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (models.UniqueConstraint(
                       fields=('user', 'recipe'),
                       name='unique_favorite_recipe',),
                       )

    def __str__(self):
        return f'{self.user} added {self.recipe}'


class ShoppingCart(models.Model):
    """Модель для корзины."""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shop_list'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт в корзине',
        on_delete=models.CASCADE,
        related_name='shop_list'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (models.UniqueConstraint(
                       fields=('user', 'recipe'),
                       name='unique_shoppings_recipe',),
                       )

    def __str__(self):
        return f'{self.user} added {self.recipe}'
