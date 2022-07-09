from django import forms
from django.forms.formsets import formset_factory

from astu_inventory.apps.store.models import Specification


class SpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = ("specification_type", "value")


SpecificationFormSet = formset_factory(SpecificationForm, extra=2)
