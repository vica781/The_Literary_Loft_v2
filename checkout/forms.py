from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone_number', 
                  'country', 'postcode', 'town_or_city', 
                  'street_address1', 'street_address2', 'county']
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        '''
        Add placeholders and classes, remove auto-generated 
        labels and set autofocus on first field
        '''
        super().__init__(*args, **kwargs)
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
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
            
                 
        
    
                         
        # labels = {
        #     'full_name': 'Full Name',
        #     'email': 'Email',
        #     'phone_number': 'Phone Number',
        #     'country': 'Country',
        #     'postcode': 'Postcode',
        #     'town_or_city': 'Town or City',
        #     'street_address1': 'Street Address 1',
        #     'street_address2': 'Street Address 2',
        #     'county': 'County'
        # }
        # widgets = {
        #     'full_name': forms.TextInput(attrs={'autofocus': True}),
        #     'email': forms.EmailInput(),
        #     'phone_number': forms.TextInput(),
        #     'country': forms.TextInput(),
        #     'postcode': forms.TextInput(),
        #     'town_or_city': forms.TextInput(),
        #     'street_address1': forms.TextInput(),
        #     'street_address2': forms.TextInput(),
        #     'county': forms.TextInput()
        # }