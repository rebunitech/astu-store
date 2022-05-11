from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from auser.mixins import (LogEntryAdditionMixin, LogEntryChangeMixin,
                          LogEntryDeletionMixin, SuperuserRequiredMixin)
from auser.utils import generate_username

UserModel = get_user_model()

from auser.signals import staff_user_created


class ListActiveStaffUsersView(SuperuserRequiredMixin, ListView):
    """Generic view used to list all staff users"""

    model = UserModel
    template_name = "auser/staff/list_active_staff_user.html"
    context_object_name = "staff_users"
    extra_context = {"title": _("Active Staff Users")}

    def get_queryset(self):
        """Return all staff users"""

        return self.model.objects.filter(
            is_staff=True, is_active=True, is_superuser=False
        )


class AddStaffUserView(
    SuperuserRequiredMixin, SuccessMessageMixin, LogEntryAdditionMixin, CreateView
):
    """Generic view used to add staff user"""

    model = UserModel
    fields = ("first_name", "last_name", "email", "phone_number", "sex")
    success_url = reverse_lazy("auser:active_staff_list")
    success_message = _("%(first_name)s %(last_name)s added successfully")
    template_name = "auser/staff/add_staff_user.html"
    extra_context = {"title": _("Add Staff User")}

    def get_success_url(self):
        x = staff_user_created.send(
            sender=self.model, instance=self.object, created=True
        )
        return super().get_success_url()

    def form_valid(self, form):
        """Set staff user to True"""
        self.object = form.save(commit=False)
        self.object.is_staff = True
        self.object.username = generate_username()
        self.object.save()
        return super().form_valid(form)


class StaffUserDetailView(SuperuserRequiredMixin, DetailView):
    model = UserModel
    template_name = "auser/staff/staff_user_detail.html"
    extra_context = {"title": _("Staff User Detail")}
    context_object_name = "staff_user"

    def get_queryset(self):
        return self.model.objects.filter(is_staff=True, is_superuser=False)

    def get_content_type(self):
        """Return content type for LogEntry"""

        return ContentType.objects.get_for_model(self.model).pk

    def get_object_hisotry(self):
        """Return log entries for the object"""

        return LogEntry.objects.filter(
            content_type_id=self.get_content_type(), object_id=self.object.pk
        )

    def get_context_data(self, **kwargs):
        kwargs.update(
            {
                "object_history": self.get_object_hisotry(),
            }
        )
        return super().get_context_data(**kwargs)


class UpdateStaffUserView(
    SuperuserRequiredMixin, SuccessMessageMixin, LogEntryChangeMixin, UpdateView
):
    """Generic view used to update staff user"""

    model = UserModel
    fields = (
        "first_name",
        "last_name",
        "email",
        "sex",
        "phone_number",
        "po_box",
        "location",
        "profile_picture",
        "bio",
    )
    success_url = reverse_lazy("auser:active_staff_list")
    success_message = _("%(first_name)s %(last_name)s updated successfully")
    template_name = "auser/staff/update_staff_user.html"
    extra_context = {"title": _("Update Staff User")}

    def get_queryset(self):
        """Return all staff users"""

        return self.model.objects.filter(
            is_staff=True, is_active=True, is_superuser=False
        )


class ListDeactivatedStaffUsersView(SuperuserRequiredMixin, ListView):
    """Generic view used to list all deactivate staff users"""

    model = UserModel
    template_name = "auser/staff/list_deactivate_staff_user.html"
    context_object_name = "deactivated_staff_users"
    extra_context = {"title": _("Deactivated Staff Users")}

    def get_queryset(self):
        """Return all deactivate staff users"""

        return self.model.objects.filter(
            is_staff=True, is_active=False, is_superuser=False
        )


class DeactivateStaffUserView(
    SuperuserRequiredMixin, SuccessMessageMixin, LogEntryChangeMixin, UpdateView
):
    """Generic view used to deactivate staff user"""

    model = UserModel
    fields = ("is_active",)
    success_url = reverse_lazy("auser:active_staff_list")
    success_message = _("%(first_name)s %(last_name)s deactivated successfully")
    http_method_names = ["post"]

    def form_valid(self, form):
        form.cleaned_data.update(
            {"first_name": self.object.first_name, "last_name": self.object.last_name}
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_active": False})
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def get_queryset(self):
        """Return all staff users"""

        return self.model.objects.filter(
            is_staff=True, is_active=True, is_superuser=False
        )


class ActivateStaffUserView(
    SuperuserRequiredMixin, SuccessMessageMixin, LogEntryChangeMixin, UpdateView
):
    """Generic view used to activate staff user"""

    model = UserModel
    fields = ("is_active",)
    success_url = reverse_lazy("auser:deactivated_staff_list")
    success_message = _("%(first_name)s %(last_name)s activated successfully")
    http_method_names = ["post"]

    def form_valid(self, form):
        form.cleaned_data.update(
            {"first_name": self.object.first_name, "last_name": self.object.last_name}
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_active": True})
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def get_queryset(self):
        """Return all deactivate staff users"""

        return self.model.objects.filter(
            is_staff=True, is_active=False, is_superuser=False
        )


class DeleteStaffUserView(SuperuserRequiredMixin, LogEntryDeletionMixin, DeleteView):
    """Generic view used to delete staff user"""

    model = UserModel
    success_url = reverse_lazy("auser:deactivated_staff_list")
    http_method_names = ["post"]

    def get_queryset(self):
        """Return all deactivate staff users"""
        return self.model.objects.filter(
            is_staff=True, is_active=False, is_superuser=False
        )
