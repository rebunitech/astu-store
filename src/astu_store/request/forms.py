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
        )
# for start borrow date and end date
# class DateRangeForm(forms.Form):
#   def __init__(self, *args, **kwargs):
#     initial_start_date = kwargs.pop('initial_start_date')
#     initial_end_date = kwargs.pop('initial_end_date')
#     required_val = kwargs.pop('required')

#     super(DateRangeForm,self).__init__(*args,**kwargs)
#     self.fields['start_date'].initial = initial_start_date
#     self.fields['start_date'].required = required_val
#     self.fields['end_date'].initial = initial_end_date
#     self.fields['end_date'].required = required_val

#   start_date = forms.DateField()
#   end_date = forms.DateField()