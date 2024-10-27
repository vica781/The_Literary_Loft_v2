from django.contrib.sitemaps import Sitemap
from .models import Book

class BookSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Book.objects.all().order_by('-updated_at') 

    def lastmod(self, obj):
        return obj.updated_at  
