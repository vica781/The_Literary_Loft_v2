from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Book

class BookSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Book.objects.all()

    def location(self, item):
        return reverse('books:book_detail', args=[item.slug])

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['books:book_list', 'books:about', 'books:contact']

    def location(self, item):
        return reverse(item)
