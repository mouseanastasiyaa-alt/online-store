from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Очищает БД и загружает тестовые данные из фикстур"

    def handle(self, *args, **options):
        self.stdout.write("Удаляем старые данные...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write("Загружаем категории...")
        call_command("loaddata", "categories.json")

        self.stdout.write("Загружаем продукты...")
        call_command("loaddata", "products.json")

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно загружены!"))
