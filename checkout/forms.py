
from django import forms
from checkout.models import Order, OrderItem



import stripe
import json


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'name',
            'email',
            'address',
            'street',            
            'city',
            'county',
            'postcode',
            'number', 
             )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'name',
            'email': 'email',
            'address': 'address',
            'street': 'street',
            'city': 'city',
            'county': 'county',
            'postcode': 'postcode',
            'number': 'number',
            
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].widget.attrs['class'] = 'stripe-style-input'
                self.fields[field].label = False