from django.forms import ModelForm, forms

from .models import *


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
