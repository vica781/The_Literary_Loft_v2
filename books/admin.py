from django.contrib import admin
from .models import Category, Subcategory, Book
from .models import Newsletter

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Book)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed', 'is_active')
    list_filter = ('is_active', 'date_subscribed')
    search_fields = ('email',)