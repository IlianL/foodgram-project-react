from django_filters.rest_framework import FilterSet, filters
from recipes.models import Ingredient, Recipe
from rest_framework import filters as f


class CustomIngredientsFilter(f.SearchFilter):
    """Фильтр для ингредиентов, параметр поиска - name.
    Filter example:
    /api/ingredients/?name=айран
    """
    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ('name',)


class CustomRecipeFilter(FilterSet):
    """Фильтр для рецептов.
    author (int) = фильтрация по полю id
    tags (int) = фильтрация по полю id
    is_favorited (bool) = булевое значение 1/0
    is_in_shopping_cart (bool) = булевое значение 1/0
    Filter example:
    /api/recipes/?tags=4&author=10&is_in_shopping_cart=0&is_favorited=1
    """
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorite_list__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(shop_list__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'author', 'is_in_shopping_cart', 'tags')
