from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User

# CATEGOTY
class Category(models.Model):
    CATEGORY_CHOICES = [
        ('fiction', 'Fiction Books'),
        ('non-fiction', 'Non-Fiction Books'),  # Change this line
        ('children', "Children's Books"),
    ]
    
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_name_display())
        super().save(*args, **kwargs)
    
    def display_name(self):
        return self.get_name_display()

    def __str__(self):
        return self.display_name()

# SUBCATEGORY
class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Subcategories"
    
    # def __str__(self):
    #     return f"{self.category.get_name_display()} - {self.name}"
    
    def save(self, *args, **kwargs):
        self.name = self.name.replace('_', '-')
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.category.display_name()} - {self.name}"
        
    def capitalized_name(self):
        return self.name.capitalize()

    def __str__(self):
        return self.capitalized_name()

# BOOK
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    about_author = CKEditor5Field(blank=True)
    isbn = models.CharField("ISBN", max_length=13)
    description = CKEditor5Field(blank=True)
    review = CKEditor5Field(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    subcategory = models.ForeignKey(Subcategory, related_name='books', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    pages = models.PositiveIntegerField(blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.subcategory.category.name not in [self.subcategory.category.name for cat in Category.objects.all()]:
            raise ValueError("Subcategory does not match the selected Category")
        super().save(*args, **kwargs)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} of {self.book.title}'
