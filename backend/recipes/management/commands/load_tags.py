from django.core.management import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    help = 'Создаем тэги'

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#F59D5D', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#9FE691', 'slug': 'dinner'},
            {'name': 'Ужин', 'color': '#C296E0', 'slug': 'supper'}]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        self.stdout.write(self.style.SUCCESS('Все тэги загружены!'))
