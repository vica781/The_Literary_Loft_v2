import json
from django.core.management.base import BaseCommand
from books.models import Book


class Command(BaseCommand):
    help = 'Load books from JSON file into the database'

    def handle(self, *args, **kwargs):
        with open('books/fixtures/books.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                Book.objects.create(
                    title=item['title'],
                    author=item['author'],
                    isbn=item['isbn'],
                    description=item['description'],
                    price=item['price'],
                    stock=item['stock'],
                    created_at=item['created_at'],
                    updated_at=item['updated_at'],
                    subcategory_id=item['subcategory_id'],
                    cover_image=item['cover_image'],
                    pages=item['pages'],
                    publication_date=item['publication_date'],
                    about_author=item['about_author'],
                    review=item['review']
                )
        self.stdout.write(
            self.style.SUCCESS('Successfully imported books data')
            )
