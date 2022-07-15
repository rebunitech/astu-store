"""ASTU Inventory auser views

Each class represents a logic layer of the project, related to department.

    Date Created: 5 July, 2022
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

from astu_inventory.apps.auser.forms import DepartmentChangeForm, DepartmentCreateForm, DepartmentHeadSelectForm
from astu_inventory.apps.auser.models import Department

UserModel = get_user_model()


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
                f"You cann't delete this college, because there is {len(error.protected_objects)} "
                "related departemnts and/or staff members for this college. try to delete related objects first.",
            )
            return HttpResponseRedirect(reverse_lazy("auser:departments_list"))


# Department Heads


class AllDepartmentHeadsListView(PermissionRequiredMixin, ListView):
    """List all department heads inside the system."""

    model = UserModel
    context_object_name = "department_heads"
    permission_required = "auser.can_list_department_heads"
    extra_context = {"title": "All Department Heads"}
    template_name = "auser/department/head/all/list.html"

    def get_queryset(self):
        return super().get_queryset().filter(Q(groups__name="department head")).exclude(Q(groups__name="college dean"))


class DepartmentHeadsListView(PermissionRequiredMixin, ListView):
    """List all department head inside specific department."""

    model = UserModel
    context_object_name = "department_heads"
    permission_required = "auser.can_list_department_heads"
    template_name = "auser/department/head/list.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="department head") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean"))
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"{self.kwargs['short_name'].upper()} department heads."})
        return context_data


class AddAllDepartmentHeadView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """Create a new department head, from all departments."""

    model = UserModel
    fields = (
        "department",
        "staff_id",
        "email",
        "sex",
        "phone_number",
    )
    permission_required = "auser.can_add_department_head"
    success_url = reverse_lazy("auser:all_department_heads_list")
    success_message = _("Department head added successfully.")
    extra_context = {"title": "Add department head"}
    template_name = "auser/department/head/all/add.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.groups.add(Group.objects.get(name="department head"))
        return response


class AddDepartmentHeadView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """Create a new department head for specific department."""

    model = UserModel
    fields = (
        "staff_id",
        "email",
        "sex",
        "phone_number",
    )
    permission_required = "auser.can_add_department_head"
    success_message = _("Department head added successfully.")
    extra_context = {"title": "Add department head"}
    template_name = "auser/department/head/add.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.department = self.department
        self.object.save()
        self.object.groups.add(Group.objects.get(name="department head"))
        return response

    def get_success_url(self):
        return reverse_lazy("auser:department_heads_list", args=[self.kwargs["short_name"]])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Add {self.kwargs['short_name'].upper()} department heads."})
        return context_data

    def setup(self, request, *args, **kwargs):
        """Check if the department with this short name exists, and save for latter use."""
        self.department = get_object_or_404(Department, short_name__iexact=kwargs["short_name"])
        super().setup(request, *args, **kwargs)


class AllSelectDepartmentHeadView(PermissionRequiredMixin, SuccessMessageMixin, FormView):
    """Select user for role of department head"""

    form_class = DepartmentHeadSelectForm
    permission_required = "auser.can_select_department_head"
    success_url = reverse_lazy("auser:all_department_heads_list")
    success_message = _('"%(user)s" selected successfully.')
    template_name = "auser/department/head/all/select.html"
    extra_context = {"title": "Select department head"}

    def form_valid(self, form):
        user = form.cleaned_data["user"]
        user.groups.add(Group.objects.get(name="department head"))
        return super().form_valid(form)


class SelectDepartmentHeadView(PermissionRequiredMixin, SuccessMessageMixin, FormView):
    """Select user for role of department head"""

    form_class = DepartmentHeadSelectForm
    permission_required = "auser.can_select_department_head"
    success_message = _('"%(user)s" selected successfully.')
    template_name = "auser/department/head/select.html"
    extra_context = {"title": "Select department head"}

    def get_success_url(self):
        return reverse_lazy("auser:department_heads_list", args=[self.kwargs["short_name"]])

    def form_valid(self, form):
        user = form.cleaned_data["user"]
        user.groups.add(Group.objects.get(name="department head"))
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form["user"].field.queryset = form["user"].field.queryset.filter(
            department__short_name__iexact=self.kwargs["short_name"]
        )
        return form


class AllDepartmentHeadUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Change existing department head profile."""

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
    success_url = reverse_lazy("auser:all_department_heads_list")
    template_name = "auser/department/head/all/update.html"
    permission_required = "auser.can_change_department_head"
    success_message = "%(first_name)s %(last_name)s updated successfully."

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="department head") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean"))
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Update {self.object.get_full_name()}"})
        return context_data


class DepartmentHeadUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Change existing department head profile."""

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
    template_name = "auser/department/head/update.html"
    permission_required = "auser.can_change_department_head"
    success_message = "%(first_name)s %(last_name)s updated successfully."

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="department head") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean"))
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Update {self.object.get_full_name()}"})
        return context_data

    def get_success_url(self):
        return reverse_lazy("auser:department_heads_list", args=[self.kwargs["short_name"]])


class AllDepartmentHeadActivateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_activate_department_head"
    success_url = reverse_lazy("auser:all_department_heads_list")
    success_message = "%(first_name)s %(last_name)s activated successfully."
    http_method_names = ["post"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(is_active=False)
                & Q(groups__name="department head")
                & Q(department__short_name__iexact=self.kwargs["short_name"])
            )
            .exclude(Q(groups__name="college dean"))
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


class DepartmentHeadActivateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_activate_department_head"
    success_message = "%(first_name)s %(last_name)s activated successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("auser:department_heads_list", args=[self.kwargs["short_name"]])

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(is_active=False)
                & Q(groups__name="department head")
                & Q(department__short_name__iexact=self.kwargs["short_name"])
            )
            .exclude(Q(groups__name="college dean"))
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


class AllDepartmentHeadDeactivateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_deactivate_department_head"
    success_url = reverse_lazy("auser:all_department_heads_list")
    success_message = "%(first_name)s %(last_name)s deactivated successfully."
    http_method_names = ["post"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(is_active=True)
                & Q(groups__name="department head")
                & Q(department__short_name__iexact=self.kwargs["short_name"])
            )
            .exclude(Q(groups__name="college dean"))
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


class DepartmentHeadDeactivateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_deactivate_department_head"
    success_message = "%(first_name)s %(last_name)s deactivated successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("auser:department_heads_list", args=[self.kwargs["short_name"]])

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(is_active=True)
                & Q(groups__name="department head")
                & Q(department__short_name__iexact=self.kwargs["short_name"])
            )
            .exclude(Q(groups__name="college dean"))
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


class AllRemoveFromDepartmentHeadView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Remove user form department head from all department heads list."""

    model = UserModel
    fields = ("groups",)
    permission_required = "auser.can_remove_department_head"
    success_message = "%(first_name)s %(last_name)s successfully removed from heads."
    success_url = reverse_lazy("auser:all_department_heads_list")
    http_method_names = ["post"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="department head") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean"))
        )

    def form_valid(self, form):
        form.cleaned_data.update({"first_name": self.object.first_name, "last_name": self.object.last_name})
        self.object.groups.remove(Group.objects.get(name="department head"))
        return super().form_valid(form)


class RemoveFromDepartmentHeadView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Remove user form department head from specifict department heads list."""

    model = UserModel
    fields = ("groups",)
    permission_required = "auser.can_remove_department_head"
    success_message = "%(first_name)s %(last_name)s successfully removed from heads."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("auser:department_heads_list", args=[self.kwargs["short_name"]])

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="department head") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean"))
        )

    def form_valid(self, form):
        form.cleaned_data.update({"first_name": self.object.first_name, "last_name": self.object.last_name})
        self.object.groups.remove(Group.objects.get(name="department head"))
        return super().form_valid(form)


class AllDepartmentHeadDeleteView(PermissionRequiredMixin, DeleteView):
    """Delete department head from the system."""

    model = UserModel
    permission_required = ("auser.can_delete_department_head",)
    success_url = reverse_lazy("auser:all_department_heads_list")
    http_method_names = ["post"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="department head") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean"))
        )

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request,
                f"Head {self.object.get_full_name()} deleted successfully.",
            )
            return response
        except ProtectedError as error:
            messages.error(
                request,
                f"You cann't delete this department head, because there is {len(error.protected_objects)} "
                "related datas. try to delete related objects first.",
            )
            return HttpResponseRedirect(self.success_url)


class DepartmentHeadDeleteView(PermissionRequiredMixin, DeleteView):
    """Delete department head from the system, from specific department heads list."""

    model = UserModel
    permission_required = ("auser.can_delete_department_head",)
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("auser:department_heads_list", args=[self.kwargs["short_name"]])

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="department head") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean"))
        )

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request,
                f"Head {self.object.get_full_name()} deleted successfully.",
            )
            return response
        except ProtectedError as error:
            messages.error(
                request,
                f"You cann't delete this department head, because there is {len(error.protected_objects)} "
                "related datas. try to delete related objects first.",
            )
            return HttpResponseRedirect(self.success_url)
