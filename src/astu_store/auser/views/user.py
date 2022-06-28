from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.views.generic import DeleteView, UpdateView

from auser.models import CollegeUser


class UpdateUserView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CollegeUser
    fields = (
        "first_name",
        "last_name",
        "username",
        "email",
        "sex",
        "phone_number",
        "college",
        "department",
    )
    permission_required = "change_collegeuser"
    template_name = "auser/update.html"


class ActivateUserView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CollegeUser
    fields = ("is_active",)
    http_method_names = ["post"]

    def get_queryset(self):
        return self.model.objects.filter(Q(is_active=False))

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_active": True})
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def form_valid(self, form):
        form.cleaned_data.update(
            {"first_name": self.object.first_name, "last_name": self.object.last_name}
        )
        return super().form_valid(form)


class DeactivateUserView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CollegeUser
    fields = ("is_active",)
    http_method_names = ["post"]

    def form_valid(self, form):
        form.cleaned_data.update(
            {"first_name": self.object.first_name, "last_name": self.object.last_name}
        )
        return super().form_valid(form)

    def get_queryset(self):
        return self.model.objects.filter(Q(is_active=True))

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_active": False})
        form_kwargs.update({"data": form_data})
        return form_kwargs


class DeleteUserView(PermissionRequiredMixin, DeleteView):
    model = CollegeUser
    http_method_names = ["post"]
