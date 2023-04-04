from core.utils_api_view import delete_or_400, make_txt_response
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (AmountIngredientInRecipe, Favorite, Ingredient,
                            Recipe, ShoppingCart, Tag)
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.models import Subscription, User

from .filters import CustomIngredientsFilter, CustomRecipeFilter
from .permissions import AdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (CreateSubscriptionRecipeSerializer,
                          FavoriteSerializer, IngredientsSerializer,
                          RecipesReadSerializer, RecipesWriteSerializer,
                          ShoppingCartSerializer, SubscriptionSerializer,
                          TagsSerializer, UserSerializer)


class TagsViewSet(ReadOnlyModelViewSet):
    """
    Добавлять/удалять/редактировать теги разрешено только администраторам.
    """
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (AdminOrReadOnly,)


class CustomUserViewSet(UserViewSet):
    """Вьюсет кастомной модели юзера."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_context(self):
        """Добавляем в контекст сет с id автора.
        Так мы решаем n+1 проблему при запросе к БД в серилизаторе."""
        try:
            subs = set(
                Subscription.objects.filter(
                    user_id=self.request.user).values_list(
                        'author_id', flat=True))
        except TypeError:
            # При регистрации
            subs = set()
        return {
            'request': self.request,
            'subscriptions': subs,
            'format': self.format_kwarg,
            'view': self
        }

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if id == request.user.id:
            return Response(
                {'error': 'Нельзя подписаться на себя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'user': user.id,
            'author': id
        }
        serializer = CreateSubscriptionRecipeSerializer(
            data=data, context=self.get_serializer_context())
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        delete_or_400(Subscription, 'Вы не подписаны на этого пользователя.',
                      user=user, author=author)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request):
        sub_list = self.paginate_queryset(
            User.objects.filter(following__user=request.user))
        serializer = SubscriptionSerializer(
            sub_list, many=True, context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)


class IngredientsViewSet(ReadOnlyModelViewSet):
    """"Работа с ингредиентами."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (CustomIngredientsFilter,)
    search_fields = ('^name',)
    pagination_class = None


class RecipesViewSet(ModelViewSet):
    """
    Работа с рецептами.
    Два серилайзера для записи и для чтения.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipesReadSerializer
    permission_classes = (
        IsAuthorOrReadOnly, permissions.IsAuthenticatedOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomRecipeFilter

    def get_serializer_context(self):
        """
        Добавляем в контекст сет с id автора, рецепта из корзины и избранного.
        Так мы решаем n+1 проблему при запросе к БД в серилизаторе."""
        subs = set(
            Subscription.objects.filter(
                user_id=self.request.user).values_list('author_id', flat=True))
        favorite_recipes = set(
            Favorite.objects.filter(
                user_id=self.request.user,
                recipe_id=self.kwargs['pk']).values_list(
                    'recipe_id', flat=True))
        shopping_cart = set(
            ShoppingCart.objects.filter(
                user_id=self.request.user,
                recipe_id=self.kwargs['pk']).values_list(
                    'recipe_id', flat=True))
        return {
            'request': self.request,
            'favorite_recipes': favorite_recipes,
            'shopping_cart': shopping_cart,
            'subscriptions': subs,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return RecipesWriteSerializer
        return RecipesReadSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        data = {
            'user': user.id,
            'recipe': pk
        }
        serializer = FavoriteSerializer(
            data=data, context=self.get_serializer_context())
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        delete_or_400(Favorite, 'У вас нет этого рецепта в избранном.',
                      user=user, recipe=recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        data = {
            'user': user.id,
            'recipe': pk
        }
        serializer = ShoppingCartSerializer(
            data=data, context=self.get_serializer_context())
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        delete_or_400(ShoppingCart, 'У вас нет этого рецепта в корзине.',
                      user=user, recipe=recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = AmountIngredientInRecipe.objects.filter(
            recipe__shop_list__user=self.request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(amount=Sum('amount'))

        return make_txt_response(ingredients)
