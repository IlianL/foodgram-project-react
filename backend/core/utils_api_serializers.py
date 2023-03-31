import base64

from rest_framework import serializers
from django.core.files.base import ContentFile


class Base64ImageField(serializers.ImageField):
    """Кастомное поле для изображений."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


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
