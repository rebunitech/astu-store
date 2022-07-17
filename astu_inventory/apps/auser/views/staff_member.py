"""ASTU Inventory auser views

Each class represents a logic layer of the project, related to staff member.

    Date Created: 14 July, 2022
    Author: Ashenafi Zenebe
"""
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from astu_inventory.apps.auser.models import Department

UserModel = get_user_model()


class AllStaffMemberListView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    """Lists of staff member form all the system."""

    model = UserModel
    template_name = "auser/staff_member/all/list.html"
    permission_required = "auser.can_list_staff_members"
    context_object_name = "staff_members"
    extra_context = {"title": "All Staff Members List"}

    def get_queryset(self):
        return super().get_queryset().filter(groups__name="staff member").exclude(Q(groups__name="college dean"))


class StaffMemberListView(ListView, PermissionRequiredMixin, SuccessMessageMixin):
    """Lists of staff members for specific department."""

    model = UserModel
    template_name = "auser/staff_member/list.html"
    permission_requeried = "auser.can_list_staff_member"
    context_object_name = "staff_members"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="staff member") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"{self.kwargs['short_name'].upper()} staff members."})
        return context_data


class AllAddStaffMemberView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """Add staff member to the system."""

    model = UserModel
    fields = (
        "department",
        "staff_id",
        "email",
        "sex",
        "phone_number",
    )
    template_name = "auser/staff_member/all/add.html"
    permission_required = "auser.can_add_staff_member"
    extra_context = {"title": "Add Staff Member"}
    success_message = _("Staff Member successfully added to the system.")
    success_url = reverse_lazy("auser:all_staff_member_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.groups.add(Group.objects.get(name="staff member"))
        return response


class AddStaffMemberView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """Add staff member into specific department."""

    model = UserModel
    fields = (
        "staff_id",
        "email",
        "sex",
        "phone_number",
    )
    permission_required = "auser.can_add_staff_member"
    template_name = "auser/staff_member/add.html"
    success_message = _("Staff member is successfully added.")
    extra_context = {"title": "Add staff member"}

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.department = self.department
        self.object.save()
        self.object.groups.add(Group.objects.get(name="staff member"))
        return response

    def get_success_url(self):
        return reverse_lazy("auser:staff_members_list", args=[self.kwargs["short_name"]])

    def setup(self, request, *args, **kwargs):
        """Check if the department with this short name exists, and save for latter use."""
        self.department = get_object_or_404(Department, short_name__iexact=kwargs["short_name"])
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Add {self.kwargs['short_name'].upper()} store officer."})
        return context_data


class AllUpdateStaffMemberView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Change existing staff member profile."""

    model = UserModel
    fields = (
        "staff_id",
        "department",
        "first_name",
        "last_name",
        "email",
        "sex",
        "phone_number",
        "location",
        "po_box",
        "profile_picture",
    )
    success_url = reverse_lazy("auser:all_staff_member_list")
    template_name = "auser/staff_member/all/update.html"
    permission_required = "auser.can_change_staff_member"
    success_message = "%(first_name)s %(last_name)s updated successfully."

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="staff member") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean"))
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Update {self.object.get_full_name()}"})
        return context_data


class UpdateStaffMemberView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update profile of staff member in specific department."""

    model = UserModel
    fields = (
        "staff_id",
        "department",
        "first_name",
        "last_name",
        "email",
        "sex",
        "phone_number",
        "location",
        "po_box",
        "profile_picture",
    )
    template_name = "auser/staff_member/update.html"
    permission_required = "auser.can_change_staff_member"
    success_message = "%(first_name)s %(last_name)s updated successfully."

    def get_success_url(self):
        return reverse_lazy("auser:staff_members_list", args=[self.kwargs["short_name"]])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Update {self.object.get_full_name()}"})
        return context_data


class AllStaffMemberActivateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Activate staff member from all of the staff member."""

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_activate_staff_member"
    success_url = reverse_lazy("auser:all_staff_member_list")
    success_message = "%(first_name)s %(last_name)s activated successfully."
    http_method_names = ["post"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(is_active=False)
                & Q(groups__name="staff member")
                & Q(department__short_name__iexact=self.kwargs["short_name"])
            )
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_active": True})
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def form_valid(self, form):
        form.cleaned_data.update({"first_name": self.object.first_name, "last_name": self.object.last_name})
        return super().form_valid(form)


class ActivateStaffMemberView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Activate staff member for specific deartment"""

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_activate_staff_member"
    success_message = "%(first_name)s %(last_name)s activated successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("auser:staff_members_list", args=[self.kwargs["short_name"]])

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(groups__name="staff member")
                & Q(is_active=False)
                & Q(department__short_name__iexact=self.kwargs["short_name"])
            )
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_active": True})
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def form_valid(self, form):
        form.cleaned_data.update({"first_name": self.object.first_name, "last_name": self.object.last_name})
        return super().form_valid(form)


class DeactivateStaffMemberView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Deactivate staff member from specific department."""

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_deactivate_staff_member"
    success_message = "%(first_name)s %(last_name)s activated successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("auser:staff_members_list", args=[self.kwargs["short_name"]])

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(is_active=True)
                & Q(groups__name="staff member")
                & Q(department__short_name__iexact=self.kwargs["short_name"])
            )
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_active": False})
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def form_valid(self, form):
        form.cleaned_data.update({"first_name": self.object.first_name, "last_name": self.object.last_name})
        return super().form_valid(form)


class AllDeactivateStaffMemberView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Deactivate staff member from all list of staff member of the system."""

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_deactivate_staff_member"
    success_message = _("%(first_name)s %(last_name)s is successfully deactivated.")
    http_method_names = ["post"]
    success_url = reverse_lazy("auser:all_staff_member_list")

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(groups__name="staff member")
                & Q(is_active=True)
                & Q(department__short_name__iexact=self.kwargs["short_name"])
            )
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_active": False})
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def form_valid(self, form):
        form.cleaned_data.update({"first_name": self.object.first_name, "last_name": self.object.last_name})
        return super().form_valid(form)


class AllStaffMemberDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    """Delete staff member from all lists of staff member of the system."""

    model = UserModel
    permission_required = "auser.can_delete_staff_member"
    success_url = reverse_lazy("auser:all_staff_member_list")
    http_method_names = ["post"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="staff member") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request,
                f"Staff member {self.object.get_full_name()} deleted successfully.",
            )
            return response
        except ProtectedError as error:
            messages.error(
                request,
                f"You cann't delete this staff member, because there is {len(error.protected_objects)} "
                "related datas. try to delete related objects first.",
            )
            return HttpResponseRedirect(self.success_url)


class DeleteStaffMemberView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    """Delete staff member from specific department."""

    model = UserModel
    permission_required = "auser.can_delete_staff_member"
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("auser:staff_members_list", args=[self.kwargs["short_name"]])

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="staff member") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request,
                f"Staff member {self.object.get_full_name()} deleted successfully. ",
            )
            return response

        except ProtectedError as error:
            messages.error(
                request,
                f"You cann't delete this store officer, because there is {len(error.protected_objects)} "
                "related datas. try to delete related objects first.",
            )
            return HttpResponseRedirect(self.success_url)


class DetailStaffMemberView(PermissionRequiredMixin, DetailView):
    """detail of staff member view logic."""

    model = UserModel
    permission_required = "auser.can_view_detail_staff_member"
    template_name = "auser/staff_member/detail.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="staff member") & Q(department__short_name__iexact=self.kwargs["short_name"]))
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Detail of {self.object.get_full_name()}"})
        return context_data
