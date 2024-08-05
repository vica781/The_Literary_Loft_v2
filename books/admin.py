from django.contrib import admin
from .models import Category, Subcategory, Book

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Book)