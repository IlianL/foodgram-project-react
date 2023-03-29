import base64

from django.core.files.base import ContentFile
from django.http.response import HttpResponse
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ParseError


class Base64ImageField(serializers.ImageField):
    """Кастомное поле для изображений."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


def serializer_with_data_content(request, pk, user, serilizer):
    """Добавляем в серилайзер дату и контекст."""
    data = {
        'user': user.id,
        'recipe': pk
    }
    serializer = serilizer(data=data, context={'request': request})
    return serializer


def create_or_400(model, text, **kwargs):
    """Создаём объект или возвращаем код 400."""
    if model.objects.filter(**kwargs).exists():
        raise ParseError(text)
    model.objects.create(**kwargs)


def delete_or_400(model, text, **kwargs):
    """"Удаляем объект или возвращаем код 400."""
    if not model.objects.filter(**kwargs).exists():
        raise ParseError(text)
    model.objects.filter(**kwargs).delete()


def make_txt_response(ingredients):
    """Отдаём список покупок в txt формате."""
    shopping_list = 'Купить в магазине:\n'
    for ingredient in ingredients:
        shopping_list += (
            f'{ingredient["ingredient__name"]}: '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]} \n'
        )
    now = timezone.now()
    file_name = f'ingredients list{now:%Y-%m-%d}'
    response = HttpResponse(shopping_list, content_type='text/plain')
    response['Content-Disposition'] = (
        f'attachment; filename="{file_name}.txt"')
    return response


def add_tags(obj, tags):
    """Добавляем тэги в рцепт."""
    for tag in tags:
        obj.tags.add(tag)


def add_ingredients(model, obj, inredients):
    """Добавляем ингредиенты в рецепт."""
    for ingredient in inredients:
        model.objects.get_or_create(
            recipe=obj,
            ingredient=ingredient['id'],
            amount=ingredient['amount']
        )
