from dataclasses import field
from pyexpat import model
from django import forms
from django.forms.formsets import formset_factory

from maintenance.models import MaintenanceRequest

class AddMaintenanceRequest(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = "__all__"

AddMaintenanceRequestSet = formset_factory(AddMaintenanceRequest, extra=2)

