"""ASTU Inventory auser views

Each class represents a logic layer of the project, related to department.

    Date Created: 5 July, 2022
    Author: Wendirad Demelash(@wendirad)
    little update by : Ashenafi Zenebe
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
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from astu_inventory.apps.auser.models import Department

UserModel = get_user_model()


class AllStoreOfficersListView(PermissionRequiredMixin, ListView):
    """List all store officers inside the system."""

    model = UserModel
    context_object_name = "store_officers"
    permission_required = "auser.can_list_store_officers"
    extra_context = {"title": "All store ofiicers"}
    template_name = "auser/department/store_officer/all/list.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="store officer"))
            .exclude(Q(groups__name="college dean") | Q(groups__name="college dean"))
        )


class StoreOfficersListView(PermissionRequiredMixin, ListView):
    """List all store officers inside specific department."""

    model = UserModel
    context_object_name = "store_officers"
    permission_required = "auser.can_list_store_officers"
    template_name = "auser/department/store_officer/list.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="store officer") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"{self.kwargs['short_name'].upper()} store officers."})
        return context_data


class AddAllStoreOfficerView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """Create a new store officer, from all departments."""

    model = UserModel
    fields = (
        "department",
        "staff_id",
        "email",
        "sex",
        "phone_number",
    )
    permission_required = "auser.can_add_store_officer"
    success_url = reverse_lazy("auser:all_store_officer_list")
    success_message = _("Store officer added successfully.")
    extra_context = {"title": "Add store officer"}
    template_name = "auser/department/store_officer/all/add.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.groups.add(Group.objects.get(name="store officer"))
        return response


class AddStoreOfficerView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """Create a new store officer for specific department."""

    model = UserModel
    fields = (
        "staff_id",
        "email",
        "sex",
        "phone_number",
    )
    permission_required = "auser.can_add_store_officer"
    success_message = _("Store officer added successfully.")
    extra_context = {"title": "Add store officer"}
    template_name = "auser/department/store_officer/add.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.department = self.department
        self.object.save()
        self.object.groups.add(Group.objects.get(name="store officer"))
        return response

    def get_success_url(self):
        # print("Sinper")
        return reverse_lazy("auser:store_officers_list", args=[self.kwargs["short_name"]])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Add {self.kwargs['short_name'].upper()} store officer."})
        return context_data

    def setup(self, request, *args, **kwargs):
        """Check if the department with this short name exists, and save for latter use."""
        self.department = get_object_or_404(Department, short_name__iexact=kwargs["short_name"])
        super().setup(request, *args, **kwargs)


class AllStoreOfficerUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Change existing store officer profile."""

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
    success_url = reverse_lazy("auser:all_store_officer_list")
    template_name = "auser/department/store_officer/all/update.html"
    permission_required = "auser.can_change_store_officer"
    success_message = "%(first_name)s %(last_name)s updated successfully."

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="store officer") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Update {self.object.get_full_name()}"})
        return context_data


class StoreOfficerUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Change existing store officer profile."""

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
    template_name = "auser/department/store_officer/update.html"
    permission_required = "auser.can_change_store_officer"
    success_message = "%(first_name)s %(last_name)s updated successfully."

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="store officer") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Update {self.object.get_full_name()}"})
        return context_data

    def get_success_url(self):
        return reverse_lazy("auser:store_officers_list", args=[self.kwargs["short_name"]])


class AllStoreOfficerActivateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_activate_store_officer"
    success_url = reverse_lazy("auser:all_store_officer_list")
    success_message = "%(first_name)s %(last_name)s activated successfully."
    http_method_names = ["post"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(is_active=False)
                & Q(groups__name="store officer")
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


class StoreOfficerActivateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_activate_store_officer"
    success_message = "%(first_name)s %(last_name)s activated successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("auser:store_officers_list", args=[self.kwargs["short_name"]])

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(is_active=False)
                & Q(groups__name="store officer")
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


class AllStoreOfficerDeactivateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_deactivate_store_officer"
    success_url = reverse_lazy("auser:all_store_officer_list")
    success_message = "%(first_name)s %(last_name)s deactivated successfully."
    http_method_names = ["post"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(is_active=True)
                & Q(groups__name="store officer")
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


class StoreOfficerDeactivateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_deactivate_store_officer"
    success_message = "%(first_name)s %(last_name)s deactivated successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        # print("ASHITI")
        return reverse_lazy("auser:store_officers_list", args=[self.kwargs["short_name"]])

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(is_active=True)
                & Q(groups__name="store officer")
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


class AllRemoveFromStoreOfficerView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Remove user form store officer from all store officers list."""

    model = UserModel
    fields = ("groups",)
    permission_required = "auser.can_remove_store_officer"
    success_message = "%(first_name)s %(last_name)s successfully removed from store officers list."
    success_url = reverse_lazy("auser:all_store_officer_list")
    http_method_names = ["post"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="store officer") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def form_valid(self, form):
        form.cleaned_data.update({"first_name": self.object.first_name, "last_name": self.object.last_name})
        self.object.groups.remove(Group.objects.get(name="store officer"))
        return super().form_valid(form)


class RemoveFromStoreOfficerView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Remove user form store officer from specifict department store officers list."""

    model = UserModel
    fields = ("groups",)
    permission_required = "auser.can_remove_store_officer"
    success_message = "%(first_name)s %(last_name)s successfully removed from heads."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("auser:store_officers_list", args=[self.kwargs["short_name"]])

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="store officer") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def form_valid(self, form):
        form.cleaned_data.update({"first_name": self.object.first_name, "last_name": self.object.last_name})
        self.object.groups.remove(Group.objects.get(name="store officer"))
        return super().form_valid(form)


class AllStoreOfficerDeleteView(PermissionRequiredMixin, DeleteView):
    """Delete store officer from the system."""

    model = UserModel
    permission_required = "auser.can_delete_store_officer"
    success_url = reverse_lazy("auser:all_store_officer_list")
    http_method_names = ["post"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="store officer") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request,
                f"Store officer {self.object.get_full_name()} deleted successfully.",
            )
            return response
        except ProtectedError as error:
            messages.error(
                request,
                f"You cann't delete this store officer, because there is {len(error.protected_objects)} "
                "related datas. try to delete related objects first.",
            )
            return HttpResponseRedirect(self.success_url)


class StoreOfficerDeleteView(PermissionRequiredMixin, DeleteView):
    """Delete store officer from the system, from specific department store officers list."""

    model = UserModel
    permission_required = "auser.can_delete_store_officer"
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("auser:store_officers_list", args=[self.kwargs["short_name"]])

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="store officer") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request,
                f"Store officer {self.object.get_full_name()} deleted successfully.",
            )
            return response
        except ProtectedError as error:
            messages.error(
                request,
                f"You cann't delete this store officer, because there is {len(error.protected_objects)} "
                "related datas. try to delete related objects first.",
            )
            return HttpResponseRedirect(self.success_url)
