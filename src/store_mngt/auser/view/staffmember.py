from auser.forms import StaffMemberRegistrationForm
from auser.mixins import (CurrentUserMixin, LogEntryAdditionMixin,
                          LogEntryChangeMixin, LogEntryDeletionMixin)
from auser.models import Staffmember
from auser.utils import generate_username
from django.contrib.admin.models import LogEntry
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

# TODO: to check signup

class SignUpView(SuccessMessageMixin, CreateView):
    model = Staffmember
    template_name = "auser/signup.html"
    form_class = StaffMemberRegistrationForm
    success_url = reverse_lazy("auser:login")
    success_message = _("Your account was created successfully. Please login.")
    extra_context = {"title": _("Sign Up")}

class AddStaffMember(CreateView, SuccessMessageMixin, PermissionRequiredMixin):
    """Generic view used to add staff member"""

    model = Staffmember
    fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "sex",
        "department",
        "location",
        "po_box",
    )
    permission_required = ("auser.add_staffmember",)  #TODO:
    template_name = "auser/staffmember/add_staff_member.html"
    success_message = _("%(first_name)s %(last_name)s added successfully")
    success_url = reverse_lazy("auser:active_staffmember_list")
    extra_context = {"title": _("Add Staff Member")}
    def form_valid(self, form):
            self.object = form.save(commit=False)
            self.object.username = generate_username()
            self.object.save()
            return super().form_valid(form)

class UpdateStaffMember( PermissionRequiredMixin, 
                            SuccessMessageMixin, UpdateView 
                            ):
    """Generic view used to update staff member. """

    model = Staffmember
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "sex",
        "location",
        "department",
        "po_box",
        "profile_picture",
        "bio",
    )
    permission_required = ("auser.change_staffmember",)
    success_url = reverse_lazy("auser:active_staffmember_list")
    template_name = "auser/staffmember/update_staff_member.html"
    success_message = _("%(first_name)s %(last_name)s updated successfully")
    extra_context = {"title": _("Update Staff Member")}

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class ListActiveStaffMembersView(PermissionRequiredMixin, ListView):
    model = Staffmember
    template_name = "auser/staffmember/list_active_staff_members.html"
    permission_required = ("auser.view_staffmember",)
    extra_context = {"title": _("Active Staff Members")}
    context_object_name = "staffmembers"

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

class ListDeactivatedStaffMembersView(PermissionRequiredMixin, ListView):
    model = Staffmember
    template_name = "auser/staffmember/list_deactivated_staff_member.html"
    permission_required = ("auser.view_staffmember",)
    extra_context = {"title": _("Deactivated Staff Member")}
    context_object_name = "deactivated_staff_members"

    def get_queryset(self):
        return self.model.objects.filter(is_active=False)


class ActivateStaffMemberView(
                               PermissionRequiredMixin,
                               SuccessMessageMixin,
                             LogEntryChangeMixin,
                               UpdateView 
                               ):
    model = Staffmember
    fields = ("is_active",)
    permission_required = ("auser.activate_staffmember",)
    success_url = reverse_lazy("auser:deactivated_staffmember_list")
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
        return self.model.objects.filter(is_active=False)


class DeactivateStaffMemberView(
                             PermissionRequiredMixin,
                              SuccessMessageMixin,
                              LogEntryChangeMixin,
                               UpdateView ):
    model = Staffmember
    permission_required = ("auser.deactivate_staffmember",)
    fields = ("is_active",)
    success_url = reverse_lazy("auser:active_staffmember_list")
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
        return self.model.objects.filter(is_active=True)



class DeleteStaffMemberView(
                            PermissionRequiredMixin,
                             SuccessMessageMixin,
                             LogEntryDeletionMixin,
                              DeleteView  ):
    model = Staffmember
    permission_required = (
        "auser.view_staffmember",
        "auser.delete_staffmember",
    )
    success_url = reverse_lazy("auser:deactivated_staffmember_list")
    http_method_names = ["post"]

    def get_queryset(self):
        return self.model.objects.filter(is_active=False)



class StaffMemberDetailView(PermissionRequiredMixin, DetailView):
    model = Staffmember
    template_name = "auser/staffmember/staff_member_detail.html"
    extra_context = {"title": _("Staff Member Detail")}
    permission_required = ("auser.view_staffmember",)
    context_object_name = "staffmember"

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
