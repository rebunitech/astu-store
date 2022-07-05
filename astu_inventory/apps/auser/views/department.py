"""ASTU Inventory auser views

Each class represents a logic layer of the project, related to department.

    Date Created: 5 July, 2022
    Author: Wendirad Demelash(@wendirad)
"""

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError, Q
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from astu_inventory.apps.auser.forms import DepartmentChangeForm, DepartmentCreateForm
from astu_inventory.apps.auser.models import Department


class ListDepartmentsView(PermissionRequiredMixin, ListView):
    """List available departments"""

    model = Department
    permission_required = "auser.can_list_departments"
    context_object_name = "departments"
    template_name = "auser/department/list.html"
    extra_context = {"title": "Departments"}


class AddDepartmentView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """Create a new department"""

    model = Department
    form_class = DepartmentCreateForm
    permission_required = "auser.add_department"
    success_url = reverse_lazy("auser:departments_list")
    success_message = _('Department "%(short_name)s" added successfully.')
    extra_context = {"title": "Add department"}
    template_name = "auser/department/add.html"


class UpdateDepartmentView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Chagnge existing department"""

    model = Department
    form_class = DepartmentChangeForm
    permission_required = "auser.change_department"
    success_url = reverse_lazy("auser:departments_list")
    success_message = _('Department "%(short_name)s" updated successfully.')
    template_name = "auser/department/update.html"
    slug_field = "short_name"
    slug_url_kwarg = "short_name"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Update {self.object.short_name}"})
        return context_data


class ActivateDepartmentView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Change department status to active."""

    model = Department
    fields = ("status",)
    permission_required = "auser.can_activate_department"
    success_url = reverse_lazy("auser:departments_list")
    success_message = _('Department "%(short_name)s" activated successfully.')
    http_method_names = ["post"]
    slug_field = "short_name"
    slug_url_kwarg = "short_name"

    def form_valid(self, form):
        form.cleaned_data.update({"short_name": self.object.short_name})
        return super().form_valid(form)

    def get_queryset(self):
        return self.model.objects.filter(Q(status=0))

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"status": 1})
        form_kwargs.update({"data": form_data})
        return form_kwargs


class DeactivateDepartmentView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Change default department status to inactive.

    Deactivating department will also deactivate it's decendants (store, lab, staffs),"""

    model = Department
    fields = ("status",)
    permission_required = "auser.can_deactivate_department"
    success_url = reverse_lazy("auser:departments_list")
    success_message = _('Department "%(short_name)s" deactivated successfully.')
    http_method_names = ["post"]
    slug_field = "short_name"
    slug_url_kwarg = "short_name"

    def form_valid(self, form):
        form.cleaned_data.update({"short_name": self.object.short_name})
        return super().form_valid(form)

    def get_queryset(self):
        return super().get_queryset().filter(Q(status=1))

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"status": 0})
        form_kwargs.update({"data": form_data})
        return form_kwargs


class DeleteDepartmentView(PermissionRequiredMixin, DeleteView):
    """Delete registerd department from the system.

    The system will prevent deleting department if there is relate
    """

    model = Department
    permission_required = "auser.delete_department"
    success_url = reverse_lazy("auser:departments_list")
    http_method_names = ["post"]
    slug_field = "short_name"
    slug_url_kwarg = "short_name"

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request,
                f"Department {self.object.short_name} deleted successfully.",
            )
            return response
        except ProtectedError as error:
            messages.error(
                request,
                f"You cann't delete this college, because there is {len(error.protected_objects)} related departemnts and/or staff members for this college. try to delete related objects first.",
            )
            return HttpResponseRedirect(reverse_lazy("auser:departments_list"))
