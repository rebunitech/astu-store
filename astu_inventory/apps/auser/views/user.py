"""ASTU Inventory auser views

Each class represents a logic layer of the project, related to every user.

    Date Created: 4 July, 2022
    Author: Wendirad Demelash(@wendirad)
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
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView

from astu_inventory.apps.auser.forms import CollegeDeanSelectForm
from astu_inventory.apps.auser.models import Department
from astu_inventory.apps.core.views import ImportView

UserModel = get_user_model()


class ProfileEditView(
    PermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    """Generic view used to update user profile"""

    model = UserModel
    fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "sex",
        "location",
        "po_box",
        "profile_picture",
    )
    success_url = reverse_lazy("auser:edit_profile")
    permission_required = ("auser.change_user",)
    template_name = "auser/profile_edit.html"
    success_message = _("Your profile updated successfully.")
    extra_context = {"title": _("Edit Profile")}

    def setup(self, request, *args, **kwargs):
        kwargs.update({"pk": request.user.pk})
        super().setup(request, *args, **kwargs)


class CollegeDeansListView(PermissionRequiredMixin, ListView):
    """List of college deans or representatives."""

    model = UserModel
    context_object_name = "college_deans"
    permission_required = "auser.can_list_college_deans"
    template_name = "auser/college_dean/list.html"
    extra_context = {"title": "College Deans"}

    def get_queryset(self):
        return super().get_queryset().filter(Q(groups__name="college dean"))


class AddCollegeDeanView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """Create a new college dean."""

    model = UserModel
    fields = (
        "department",
        "staff_id",
        "email",
        "sex",
        "phone_number",
    )
    permission_required = "auser.can_add_college_dean"
    success_url = reverse_lazy("auser:college_deans_list")
    success_message = _("College dean added successfully.")
    extra_context = {"title": "Add collge dean"}
    template_name = "auser/college_dean/add.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.groups.add(Group.objects.get(name="college dean"))
        return response


class SelectCollegeDeanView(PermissionRequiredMixin, SuccessMessageMixin, FormView):
    """Select user for role of college dean"""

    form_class = CollegeDeanSelectForm
    permission_required = "auser.can_select_college_dean"
    success_url = reverse_lazy("auser:college_deans_list")
    success_message = _('"%(user)s" selected successfully.')
    template_name = "auser/college_dean/select.html"
    extra_context = {"title": "Select collge dean"}

    def form_valid(self, form):
        user = form.cleaned_data["user"]
        user.groups.add(Group.objects.get(name="college dean"))
        return super().form_valid(form)


class CollegeDeanUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Change existing college dean profile."""

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
    success_url = reverse_lazy("auser:college_deans_list")
    template_name = "auser/college_dean/update.html"
    permission_required = "auser.can_change_college_dean"
    success_message = "%(first_name)s %(last_name)s updated successfully."

    def get_queryset(self):
        return super().get_queryset().filter(Q(groups__name="college dean"))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Update {self.object.get_full_name()}"})
        return context_data


class CollegeDeanActivateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Disbale a college representative from authentication."""

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_activate_college_dean"
    success_url = reverse_lazy("auser:college_deans_list")
    success_message = "%(first_name)s %(last_name)s activated successfully."
    http_method_names = ["post"]

    def get_queryset(self):
        return super().get_queryset().filter(Q(is_active=False) & Q(groups__name="college dean"))

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_active": True})
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def form_valid(self, form):
        form.cleaned_data.update({"first_name": self.object.first_name, "last_name": self.object.last_name})
        return super().form_valid(form)


class CollegeDeanDeactivateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Change status of college dean, disable from authentication."""

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_deactivate_college_dean"
    success_url = reverse_lazy("auser:college_deans_list")
    success_message = "%(first_name)s %(last_name)s deactivated successfully."
    http_method_names = ["post"]

    def get_queryset(self):
        return super().get_queryset().filter(Q(is_active=True) & Q(groups__name="college dean"))

    def form_valid(self, form):
        form.cleaned_data.update({"first_name": self.object.first_name, "last_name": self.object.last_name})
        return super().form_valid(form)


class RemoveFromCollegeDeanView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Remove user form college deans list."""

    model = UserModel
    fields = ("groups",)
    permission_required = "auser.can_remove_college_dean"
    success_message = "%(first_name)s %(last_name)s successfully removed from deans."
    success_url = reverse_lazy("auser:college_deans_list")
    http_method_names = ["post"]

    def get_queryset(self):
        return super().get_queryset().filter(Q(groups__name="college dean"))

    def form_valid(self, form):
        form.cleaned_data.update({"first_name": self.object.first_name, "last_name": self.object.last_name})
        self.object.groups.remove(Group.objects.get(name="college dean"))
        return super().form_valid(form)


class CollegeDeanDeleteView(PermissionRequiredMixin, DeleteView):
    """Remove college dean from the system."""

    model = UserModel
    permission_required = ("auser.can_delete_college_dean",)
    success_url = reverse_lazy("auser:college_deans_list")
    http_method_names = ["post"]

    def get_queryset(self):
        return super().get_queryset().filter(Q(groups__name="college dean"))

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request,
                f"Dean {self.object.get_full_name()} deleted successfully.",
            )
            return response
        except ProtectedError as error:
            messages.error(
                request,
                f"You cann't delete this college dean, because there is {len(error.protected_objects)} "
                "related datas. try to delete related objects first.",
            )
            return HttpResponseRedirect(self.success_url)


class ImportStaffMembersView(PermissionRequiredMixin, ImportView):
    model = UserModel
    required_fields = ["Staff ID", "Email", "Phone number"]
    db_field_name = ["staff_id", "email", "phone_number", "department"]
    permission_required = "auser.can_import_staff_member"
    object_types = {"Phone number": "string"}

    @staticmethod
    def run_on_object(user):
        user.groups.add(Group.objects.get(name="staff member"))

    def get_phone_number_format(self, workbook):
        return workbook.add_format({"num_format": "@"})

    def post(self, request, *args, **kwargs):
        self.department = get_object_or_404(Department, short_name__iexact=self.kwargs["short_name"])
        return super().post(request, *args, **kwargs)

    def get_defaults(self):
        return {"department": self.department}
