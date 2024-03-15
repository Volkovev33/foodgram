import os
import json

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'Загрузка из json'

    def add_arguments(self, parser):
        parser.add_argument('filename', default='ingredients.json', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        with open(os.path.join(DATA_ROOT, options['filename']), 'r',
                  encoding='utf-8') as file:
            reader = json.load(file)
            Ingredient.objects.bulk_create(
                Ingredient(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('json успешно загружен!'))
