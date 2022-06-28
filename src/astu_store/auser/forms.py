from django import forms
from django.contrib.auth.forms import UserCreationForm as UCForm
from django.db.models import Q

from auser.models import College, CollegeUser, Department


class CollegeForm(forms.ModelForm):
    class Meta:
        model = College
        fields = (
            "name",
            "short_name",
            "description",
        )

    def clean_short_name(self):
        return self.cleaned_data["short_name"].upper().replace(" ", "")


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = (
            "name",
            "short_name",
            "description",
        )

    def clean_short_name(self):
        return self.cleaned_data["short_name"].upper().replace(" ", "")


class UserCreateForm(UCForm):
    class Meta:
        model = CollegeUser
        fields = (
            "department",
            "username",
            "email",
            "sex",
            "phone_number",
            "password1",
            "password2",
        )
