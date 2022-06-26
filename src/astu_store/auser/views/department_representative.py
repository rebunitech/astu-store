from django.contrib.auth.mixins import (
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin


from django.urls import reverse_lazy
from django.views.generic import (CreateView)

from auser.mixins import (ActiveCollegeRequiredMixin,
                          CreateUserMixin)
from auser.models import CollegeUser


class AddDepartmentRepresentativeView(
    PermissionRequiredMixin,
    SuccessMessageMixin,
    ActiveCollegeRequiredMixin,
    CreateUserMixin,
    CreateView,
):
    model = CollegeUser
    fields = (
        "college",
        "department",
        "email",
        "sex",
        "phone_number",
    )
    permission_required = "auser.can_add_department_representative"
    user_object_name = "department head"
    groups = ["department_representative"]

    def get_success_url(self):
        return reverse_lazy(
            "auser:list_departments_for_college", args=[self.kwargs["short_name"]]
        )
