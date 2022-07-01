from django import forms

from core.models import Reason


class ReasonForm(forms.ModelForm):
    class Meta:
        model = Reason
        fields = ("description",)
