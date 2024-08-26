from django import forms
from .models import Order
import json
import os
from django.conf import settings

class OrderForm(forms.ModelForm):
    country = forms.ChoiceField(
        choices=[], 
        widget=forms.Select(attrs={'id': 'country', 'name': 'country'})
    )

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone_number', 
                  'country', 'postcode', 'town_or_city', 
                  'street_address1', 'street_address2', 'county']
        widgets = {
            'full_name': forms.TextInput(attrs={'id': 'full_name', 'name': 'full_name'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'name': 'email'}),
            'phone_number': forms.TextInput(attrs={'id': 'phone_number', 'name': 'phone_number'}),
            'postcode': forms.TextInput(attrs={'id': 'postcode', 'name': 'postcode'}),
            'town_or_city': forms.TextInput(attrs={'id': 'town_or_city', 'name': 'town_or_city'}),
            'street_address1': forms.TextInput(attrs={'id': 'street_address1', 'name': 'street_address1'}),
            'street_address2': forms.TextInput(attrs={'id': 'street_address2', 'name': 'street_address2'}),
            'county': forms.TextInput(attrs={'id': 'county', 'name': 'county'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Load country data from the JSON file
        json_file_path = os.path.join(settings.STATIC_ROOT, 'json/countries.json')
        with open(json_file_path) as f:
            countries = json.load(f)
        
        # Create a list of tuples with country code and name
        country_list = [(country['code'], country['country']) for country in countries]
        
        # Set the choices for the country field
        self.fields['country'].choices = [('', '--Select a country--')] + country_list
            
        # Setting placeholders and CSS classes for fields
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postcode',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County'
        }
        
        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            placeholder = placeholders[field] + (' *' if self.fields[field].required else '')
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
