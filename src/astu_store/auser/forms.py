from django import forms
from django.contrib.auth.forms import UserCreationForm as UCForm
from django.db.models import Q

from auser.models import College, CollegeUser, Department


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


class AssignCollegeRepresentativeForm(forms.Form):
    college = forms.ChoiceField(
        choices=College.objects.values_list("id", "name"),
        widget=forms.Select(attrs={"class": "choices"}),
    )
    user = forms.ChoiceField(
        choices=CollegeUser.objects.filter(
            ~Q(groups__name="college_representative"), Q(is_active=True)
        ).values_list("id", "username"),
        widget=forms.Select(attrs={"class": "choices"}),
    )


class AssignDeprtmentRepresentativeForm(forms.Form):
    college = forms.ChoiceField(
        choices=College.objects.values_list("id", "name"),
        widget=forms.Select(attrs={"class": "choices"}),
    )
    department = forms.ChoiceField(
        choices=Department.objects.values_list("id", "name"),
        widget=forms.Select(attrs={"class": "choices"}),
    )
    user = forms.ChoiceField(
        choices=(
            (ID, " ".join(detail))
            for ID, *detail in CollegeUser.objects.filter(
                Q(is_active=True)
            ).values_list("id", "first_name", "last_name", "username")
        ),
        widget=forms.Select(attrs={"class": "choices"}),
    )
