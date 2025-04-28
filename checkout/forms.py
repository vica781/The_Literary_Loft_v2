from django import forms
from .models import Order
import json
import os
from django.conf import settings
from django.contrib.auth.models import User
import re

class OrderForm(forms.ModelForm):
    country = forms.ChoiceField(
        choices=[], 
        widget=forms.Select(attrs={'id': 'country', 'name': 'country'})
    )
    save_info = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())

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
        
        json_file_path = os.path.join(settings.STATIC_ROOT, 'json/countries.json')
        with open(json_file_path) as f:
            countries = json.load(f)
        
        country_list = [(country['code'], country['country']) for country in countries]
        self.fields['country'].choices = [('', '--Select a country--')] + country_list
            
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
        
        self.fields['save_info'].widget.attrs['class'] = 'form-check-input'
        self.fields['save_info'].label = 'Save this information for next time'
        
        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field in placeholders:
                placeholder = placeholders[field] + (' *' if self.fields[field].required else '')
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].widget.attrs['class'] = 'stripe-style-input'
                self.fields[field].label = False

    # Validators
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or '@' not in email:
            raise forms.ValidationError('Please enter a valid email address.')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^\+?[\d\s\-]+$', phone_number):
            raise forms.ValidationError('Please enter a valid phone number.')
        return phone_number

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if not country:
            raise forms.ValidationError('Please select a country.')
        return country

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not full_name or len(full_name.strip()) < 2:
            raise forms.ValidationError('Please enter your full name.')
        return full_name

    def clean_postcode(self):
        postcode = self.cleaned_data.get('postcode')
        if not postcode:
            raise forms.ValidationError('Please enter your postcode.')
        return postcode

    def clean_town_or_city(self):
        town_or_city = self.cleaned_data.get('town_or_city')
        if not town_or_city:
            raise forms.ValidationError('Please enter your town or city.')
        return town_or_city

    def clean_street_address1(self):
        street_address1 = self.cleaned_data.get('street_address1')
        if not street_address1:
            raise forms.ValidationError('Please enter street address 1.')
        return street_address1

class ReadOnlyEmailWidget(forms.TextInput):
    def __init__(self, attrs=None):
        default_attrs = {'readonly': 'readonly'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

class CustomUserChangeForm(forms.ModelForm):
    email = forms.EmailField(widget=ReadOnlyEmailWidget())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'First Name',
            'autofocus': True,
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Last Name',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['email'].help_text = 'If you need to change your email address, please contact support.'

    # Validators
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and len(first_name.strip()) < 2:
            raise forms.ValidationError('First name must be at least 2 characters long.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and len(last_name.strip()) < 2:
            raise forms.ValidationError('Last name must be at least 2 characters long.')
        return last_name
