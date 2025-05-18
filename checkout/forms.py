from django import forms
from .models import Order
import json
import os
from django.conf import settings
import re
from django.contrib.auth.models import User


class OrderForm(forms.ModelForm):
    country = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'id': 'country',})
    )
    save_info = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput()
        )
    set_default_info = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput())

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone_number',
                  'country', 'postcode', 'town_or_city',
                  'street_address1', 'street_address2', 'county']

        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'id': 'full_name',
                    }
                ),
            'email': forms.EmailInput(
                attrs={
                    'id': 'email',
                    }
                ),
            'phone_number': forms.TextInput(
                attrs={
                    'id': 'phone_number',
                    }
                ),
            'postcode': forms.TextInput(
                attrs={
                    'id': 'postcode',
                    }
                ),
            'town_or_city': forms.TextInput(
                attrs={
                    'id': 'town_or_city',
                    }
                ),
            'street_address1': forms.TextInput(
                attrs={
                    'id': 'street_address1',
                    }
                ),
            'street_address2': forms.TextInput(
                attrs={
                    'id': 'street_address2',
                    }
                ),
            'county': forms.TextInput(
                attrs={'id': 'county',
                       }
                ),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        json_file_path = os.path.join(
            settings.STATIC_ROOT,
            'json/countries.json'
            )
        with open(json_file_path) as f:
            countries = json.load(f)

        country_list = [
            (country['code'], country['country']) for country in countries
            ]
        self.fields['country'].choices = [
            ('', '--Select a country--')] + country_list

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email',
            'phone_number': 'Phone Number',
            # 'country': 'Country',
            'postcode': 'Postcode',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County'
        }

        self.fields['save_info'].widget.attrs['class'] = (
            'form-check-input'
        )
        self.fields['save_info'].label = (
            'Save this delivery information for next time'
        )

        self.fields['set_default_info'].widget.attrs['class'] = (
            'form-check-input'
        )
        self.fields['set_default_info'].label = (
            'Set this address as my default address'
        )

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field in placeholders:
                placeholder = placeholders[field]
                if self.fields[field].required:
                    placeholder += ' *'
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].widget.attrs['class'] = (
                    'stripe-style-input'
                )
                self.fields[field].label = False


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
        self.fields['email'].help_text = (
            'If you need to change your email address, please contact support.'
            )

    # Validators
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and len(first_name.strip()) < 2:
            raise forms.ValidationError(
                'First name must be at least 2 characters long.'
                )
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and len(last_name.strip()) < 2:
            raise forms.ValidationError(
                'Last name must be at least 2 characters long.'
                )
        return last_name
