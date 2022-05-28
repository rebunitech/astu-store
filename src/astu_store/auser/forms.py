from django.contrib.auth.forms import UserCreationForm as UCForm

from auser.models import CollegeUser


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
