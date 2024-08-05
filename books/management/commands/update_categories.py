from django.core.management.base import BaseCommand
from books.models import Category, Subcategory  # Replace 'books' with your actual app name

class Command(BaseCommand):
    help = 'Updates category and subcategory names and slugs'

    def handle(self, *args, **options):
        for category in Category.objects.all():
            category.save()
            self.stdout.write(self.style.SUCCESS(f'Updated category: {category}'))

        for subcategory in Subcategory.objects.all():
            old_name = subcategory.name
            subcategory.name = subcategory.name.replace('_', '-')
            subcategory.save()
            self.stdout.write(self.style.SUCCESS(f'Updated subcategory: {old_name} -> {subcategory.name}'))

        self.stdout.write(self.style.SUCCESS('Update complete!'))