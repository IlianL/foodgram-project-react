
from core.utils import Base64ImageField, add_ingredients, add_tags
from recipes.models import (AmountIngredientInRecipe, Favorite, Ingredient,
                            Recipe, ShoppingCart, Tag)
from rest_framework import serializers, validators
from users.models import Subscription, User


class TagsSerializer(serializers.ModelSerializer):
    """Сериалайзер для тэгов"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('__all__',)


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для пользователя."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def get_is_subscribed(self, obj):
        """Проверка подписки на пользователей."""
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and Subscription.objects.filter(user=user, author=obj.id).exists()
        )

    def create(self, validated_data):
        """ Создаём нового пользователя."""
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class IngredientsSerializer(serializers.ModelSerializer):
    """Серилайзер для ингредиентов"""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('__all__',)


class ReadAmountIngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериайзер для вывода количество ингредиентов в рецепте."""

    id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='ingredient')

    name = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='name',
        read_only=True)

    measurement_unit = serializers.SlugRelatedField(
        source='ingredient',
        read_only=True,
        slug_field='measurement_unit'
    )

    class Meta:
        model = AmountIngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipesReadSerializer(serializers.ModelSerializer):
    """Только чтение, возвращает список рецептов"""
    tags = TagsSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = ReadAmountIngredientInRecipeSerializer(
        many=True,
        # А почему в прошлых  вложенных серилайзерах источник не нужен был?
        source='ingredient_list')
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        """Находится ли рецепт в избранном."""
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and request.user.favorite_list.filter(recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        """Находится ли рецепт в списке покупок."""
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and request.user.shop_list.filter(recipe=obj).exists())


class WriteAmountIngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания ингредиентов в рецепте."""
    # Я правильно понмаю если в рилейтед поле есть
    # кверисет то оно используется только для записи
    # а для оборажения поле id берут из модели указанной в мета?
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = AmountIngredientInRecipe
        fields = ('id', 'amount')

    def to_representation(self, instance):
        """Отображаем поля:'id', 'name', 'measurement_unit', 'amount'."""

        serializer = ReadAmountIngredientInRecipeSerializer(instance)
        return serializer.data


class RecipesWriteSerializer(serializers.ModelSerializer):
    """Сериалайзер для записи рецета."""

    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    author = UserSerializer(read_only=True)
    ingredients = WriteAmountIngredientInRecipeSerializer(
        many=True,
        source='ingredient_list')
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time')

    def create(self, validated_data):
        ingredint_list = validated_data.pop('ingredient_list')
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.save()
        add_tags(recipe, tags)
        add_ingredients(AmountIngredientInRecipe, recipe, ingredint_list)

        return recipe

    def update(self, instance, validated_data):
        ingredint_list = validated_data.pop('ingredient_list')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        add_tags(instance, tags)
        instance.ingredient.clear()
        add_ingredients(AmountIngredientInRecipe, instance, ingredint_list)
        return super().update(instance, validated_data)


class SubscriptionRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для коротких рецептов в SubscriptionSerializer."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('__all__',)


class SubscriptionSerializer(UserSerializer):

    recipes = SubscriptionRecipeSerializer(read_only=True, many=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('email', 'username', 'last_name', 'first_name',)

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe'],
            )
        ]

    def to_representation(self, instance):
        return SubscriptionRecipeSerializer(instance.recipe).data


class ShoppingCartSerializer(FavoriteSerializer):

    class Meta(FavoriteSerializer.Meta):
        model = ShoppingCart
        validators = [
            validators.UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['user', 'recipe'],
            )
        ]

    def to_representation(self, instance):
        serializer = SubscriptionRecipeSerializer(instance.recipe)
        return serializer.data
