"""ASTU Inventory auser views

Each class represents a single form.

    Date Created: 4 July, 2022
    Author: Wendirad Demelash(@wendirad)
"""
from django import forms
from django.contrib.auth.models import Group, Permission

class ChangePermissionForm(forms.ModelForm):
    """Form used to change roles's permission

    Avoid a major performance hit resolving permission names which
    triggers a content_type load:
    """

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related('content_type'), required=False
    )

    class Meta:
        model = Group
        fields = ("permissions",)

