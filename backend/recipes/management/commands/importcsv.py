import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = "import data from ingredients.csv and tags.csv"

    def handle(self, *args, **options):
        """Импортер данных из csv."""
        # Импортируем ингредиенты.
        with open('data/ingredients.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                name, measurement_unit = row
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=measurement_unit
                )
            print(f'Файл {csvfile.name} загружен.')
        # Импортируем тэги.
        with open('data/tags.csv', encoding='utf-8') as csvfile:
            reader_tags = csv.reader(csvfile)
            for row in reader_tags:
                name, color, slug = row
                Tag.objects.get_or_create(name=name,
                                          color=color,
                                          slug=slug)
            print(f'Файл {csvfile.name} загружен.')
