from django.contrib import admin

from .models import (AmountIngredientInRecipe, Favorite, Ingredient, Recipe,
                     ShoppingCart, Tag)

admin.site.site_header = 'Администрирование Foodgram'
EPMTY_VALUE = 'Тут ничего нет :('


class AmountIngredientInRecipeInline(admin.TabularInline):
    model = AmountIngredientInRecipe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name', 'slug',)
    list_filter = ('name',)
    ordering = ('name', 'id',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('name', 'measurement_unit',)
    list_filter = ('measurement_unit',)
    ordering = ('name', 'id',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'pub_date', 'name', 'text', 'cooking_time',
                    'get_tags', 'get_ingredients', 'count_favorites',)
    readonly_fields = ('count_favorites',)
    search_fields = ('name', 'cooking_time')
    list_filter = ('cooking_time',)
    empty_value_display = EPMTY_VALUE
    ordering = ('name', 'id',)
    inlines = (AmountIngredientInRecipeInline,)

    @admin.display(description='Количество добавлений в избранное')
    def count_favorites(self, obj):
        """Общее число добавлений этого рецепта в избранное."""
        return obj.favorite_list.count()

    @admin.display(description='Тэги')
    def get_tags(self, obj):
        """Все тэги этого рецепта."""
        return ', '.join(tag.name for tag in obj.tags.all())

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        """Все ингредиенты этого рецепта."""
        return ', '.join(
            ingredient.name for ingredient
            in obj.ingredient.all())


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = EPMTY_VALUE


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', )
    list_filter = ('user', 'recipe',)
    empty_value_display = EPMTY_VALUE
