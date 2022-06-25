from dataclasses import field
from pyexpat import model
from django import forms
from django.forms.formsets import formset_factory

from maintenace.models import MaintenanceRequest

class AddMaintenaceRequest(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = "__all__"

AddMaintenaceRequestSet = formset_factory(AddMaintenaceRequest, extra=2)

