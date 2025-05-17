'''Books App Forms'''

from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    '''Book Form'''
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'about_author', 'isbn', 'description',
            'review', 'price', 'stock', 'subcategory', 'cover_image',
            'pages', 'publication_date'
        ]


class ContactForm(forms.Form):
    '''Contact Form'''
    name = forms.CharField(max_length=100, required=True, label="Name")
    email = forms.EmailField(required=True, label="Email")
    subject = forms.CharField(max_length=150, required=True, label="Subject")
    message = forms.CharField(
        widget=forms.Textarea,
        required=True,
        label="Message"
    )
