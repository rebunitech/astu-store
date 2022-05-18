"""ASTU store management auser form
	
    Created by: Ashenafi Zenebe
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       UsernameField)
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

from auser.models import Staffmember


UserModel = get_user_model()

# TODO: check this also
class StaffMemberRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Staffmember
        fields = ("username", "email", "first_name", "last_name", "phone_number", "sex")


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


# class StudentRegistrationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = Student
#         fields = ("username", "email", "first_name", "last_name", "phone_number", "sex")


