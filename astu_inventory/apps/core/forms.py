from django import forms

from astu_inventory.apps.core.models import Reason


class ReasonForm(forms.ModelForm):
    class Meta:
        model = Reason
        fields = ("description",)
