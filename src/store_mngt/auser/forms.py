"""gradient_infosys auser URL Configuration
	
    Created by: Wendirad Demelash
    Last modified by: Wendirad Demelash
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       UsernameField)
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

# from auser.models import EducationBackground, Student, Experience
from auser.models import Student

UserModel = get_user_model()


class UserChangeForm(forms.ModelForm):
    """Model form used to update user profile"""

    class Meta:
        model = UserModel
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "sex",
            "location",
            "po_box",
            "profile_picture",
            "bio",
        )
        field_classes = {"username": UsernameField}


class LoginForm(AuthenticationForm):
    """Form used to login"""

    class Meta:
        labels = {"username", _("Username or email")}


class ChangePermissionForm(forms.ModelForm):
    """Form used to change user's permission"""

    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(), required=False
    )

    class Meta:
        model = UserModel
        fields = ("user_permissions",)


class StudentRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Student
        fields = ("username", "email", "first_name", "last_name", "phone_number", "sex")


# class EducationBackgroundForm(forms.ModelForm):
#     class Meta:
#         model = EducationBackground
#         fields = (
#             "institution_name",
#             "institution_location",
#             "degree_level",
#             "major",
#             "start_year",
#             "end_year",
#             "description",
#             "completed",
#         )
#         widgets = {
#             "completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
#         }

# class ExperienceForm(forms.ModelForm):
#     class Meta:
#         model = Experience
#         fields = (
#             "company_name",
#             "company_location",
#             "job_title",
#             "start_year",
#             "end_year",
#             "description",
#             "volunteer",
#         )
#         widgets = {
#             "volunteer": forms.CheckboxInput(attrs={"class": "form-check-input"}),
#         }