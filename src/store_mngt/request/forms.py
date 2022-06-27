from wsgiref.util import request_uri
from django.forms import ModelForm, forms

from .models import *
from django.core.exceptions import ValidationError
from .models import Item, Request 

class AddRequestView(ModelForm):
    class Meta:
        model = Request
        fields = (
            "item",
            "quantity",
            "start_date",
            "end_date",
            "category",
        )
    
    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        if self.request.item.quantity >  data:
            raise ValidationError("You entered more than the available !")
        return data    

