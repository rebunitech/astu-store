"""ASTU Inventory auser views

Each class represents a single form.

    Date Created: 4 July, 2022
    Author: Wendirad Demelash(@wendirad)
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.validators import ValidationError
from django.db.models import Q

from astu_inventory.apps.auser.models import Department

UserModel = get_user_model()


class ChangePermissionForm(forms.ModelForm):
    """Form used to change roles's permission

    Avoid a major performance hit resolving permission names which
    triggers a content_type load:
    """

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related("content_type"), required=False
    )

    class Meta:
        model = Group
        fields = ("permissions",)


class DepartmentCreateForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = (
            "name",
            "short_name",
            "description",
        )

    def clean_short_name(self):
        short_name = self.cleaned_data["short_name"]
        if Department.objects.filter(short_name__iexact=short_name).exists():
            raise ValidationError("Department with this short name exists.")
        return short_name


class DepartmentChangeForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ("name", "short_name", "description")

    def clean_short_name(self):
        short_name = self.cleaned_data["short_name"]
        if Department.objects.filter(short_name__iexact=short_name).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Department with this short name exists.")
        return short_name


class CollegeDeanSelectForm(forms.Form):
    """Used to select users for a role college dean."""

    user = forms.ModelChoiceField(queryset=UserModel.objects.exclude(groups__name="college dean"))


class DepartmentHeadSelectForm(forms.Form):
    """Used to select users for a role department head."""

    user = forms.ModelChoiceField(
        queryset=UserModel.objects.exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
    )
