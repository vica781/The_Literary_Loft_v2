from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'about_author', 'isbn', 'description',
            'review', 'price', 'stock', 'subcategory', 'cover_image',
            'pages', 'publication_date'
        ]
