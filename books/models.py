from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('fiction', 'Fiction Books'),
        ('non_fiction', 'Non-Fiction Books'),
        ('children', "Children's Books"),
    ]
    
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.get_name_display()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_name_display())
        super().save(*args, **kwargs)

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Subcategories"
    
    def __str__(self):
        return f"{self.category.get_name_display()} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField("ISBN", max_length=13, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    subcategory = models.ForeignKey(Subcategory, related_name='books', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title