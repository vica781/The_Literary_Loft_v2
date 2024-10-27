from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap  
from books.sitemaps import BookSitemap  
from django.views.generic import TemplateView

# Sitemaps dictionary
sitemaps = {
    'books': BookSitemap,
    'static': GenericSitemap,  
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('books.urls')),  # the books app URLs
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('checkout/', include('checkout.urls')),  # the checkout app URLs

    # Sitemap and robots.txt
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
