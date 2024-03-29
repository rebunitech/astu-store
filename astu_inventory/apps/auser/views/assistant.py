"""
    Date Created: 16 July, 2022
    Author: Getabalew Temesgen
    updated by : Ashenafi Zenebe (sinper)

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


class AllLabAssistantListView(PermissionRequiredMixin, ListView):
    """List all Lab Assistant inside the system."""

    model = UserModel
    context_object_name = "lab_assistants"
    permission_required = "auser.can_list_all_lab_assistant"
    extra_context = {"title": "All Lab Assistant"}
    template_name = "auser/department/lab_assistant/all/list.html"
    paginated_by = 50

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="lab assistant"))
            .exclude(Q(groups__name="college dean") | Q(groups__name="college dean"))
        )


class LabAssistantListView(PermissionRequiredMixin, ListView):
    """List all lab assistant inside specific department."""

    model = UserModel
    context_object_name = "lab_assistants"
    permission_required = "auser.can_list_lab_assistant"
    template_name = "auser/department/lab_assistant/list.html"
    paginated_by = 50

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="lab assistant") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"{self.kwargs['short_name'].upper()} lab assistant."})
        return context_data


class AddAllLabAssistantView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """Create a new lab assistant, from all departments."""

    model = UserModel
    fields = (
        "department",
        "staff_id",
        "email",
        "sex",
        "phone_number",
    )
    permission_required = "auser.can_add_lab_assistant"
    success_url = reverse_lazy("auser:all_lab_assistants_list")
    success_message = _("Lab Assistant added successfully.")
    extra_context = {"title": "Add Lab Assistant"}
    template_name = "auser/department/lab_assistant/all/add.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.groups.add(Group.objects.get(name="lab assistant"))
        return response


class AddLabAssistantView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """Create a new lab assistant for specific department."""

    model = UserModel
    fields = (
        "staff_id",
        "email",
        "sex",
        "phone_number",
    )
    permission_required = "auser.can_add_lab_assistant"
    success_message = _("Lab Assistant added successfully.")
    extra_context = {"title": "Add Lab Assistant"}
    template_name = "auser/department/lab_assistant/add.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.department = self.department
        self.object.save()
        self.object.groups.add(Group.objects.get(name="lab assistant"))
        return response

    def get_success_url(self):
        return reverse_lazy("auser:lab_assistants_list", args=[self.kwargs["short_name"]])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Add {self.kwargs['short_name'].upper()} lab assistant."})
        return context_data

    def setup(self, request, *args, **kwargs):
        """Check if the department with this short name exists, and save for latter use."""
        self.department = get_object_or_404(Department, short_name__iexact=kwargs["short_name"])
        super().setup(request, *args, **kwargs)


class AllLabAssistantUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Change existing lab assistant profile."""

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
    success_url = reverse_lazy("auser:all_lab_assistants_list")
    template_name = "auser/department/lab_assistant/all/update.html"
    permission_required = "auser.can_change_lab_assistant"
    success_message = "%(first_name)s %(last_name)s updated successfully."

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="lab assistant") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Update {self.object.get_full_name()}"})
        return context_data


class LabAssistantUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Change existing lab assistant profile."""

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
    template_name = "auser/department/lab_assistant/update.html"
    permission_required = "auser.can_change_lab_assistant"
    success_message = "%(first_name)s %(last_name)s updated successfully."

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="lab assistant") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Update {self.object.get_full_name()}"})
        return context_data

    def get_success_url(self):
        return reverse_lazy("auser:lab_assistants_list", args=[self.kwargs["short_name"]])


class AllLabAssistantActivateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_activate_lab_assistant"
    success_url = reverse_lazy("auser:all_lab_assistants_list")
    success_message = "%(first_name)s %(last_name)s activated successfully."
    http_method_names = ["post"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(is_active=False)
                & Q(groups__name="lab assistant")
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


class LabAssistantActivateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_activate_lab_assistant"
    success_message = "%(first_name)s %(last_name)s activated successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("auser:lab_assistants_list", args=[self.kwargs["short_name"]])

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(is_active=False)
                & Q(groups__name="lab assistant")
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


class AllLabAssistantDeactivateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_deactivate_lab_assistant"
    success_url = reverse_lazy("auser:all_lab_assistants_list")
    success_message = "%(first_name)s %(last_name)s deactivated successfully."
    http_method_names = ["post"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(is_active=True)
                & Q(groups__name="lab assistant")
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


class LabAssistantDeactivateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):

    model = UserModel
    fields = ("is_active",)
    permission_required = "auser.can_deactivate_lab_assistant"
    success_message = "%(first_name)s %(last_name)s deactivated successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("auser:lab_assistants_list", args=[self.kwargs["short_name"]])

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(is_active=True)
                & Q(groups__name="lab assistant")
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


class AllRemoveFromLabAssistantView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Remove user from all lab assistant list."""

    model = UserModel
    fields = ("groups",)
    permission_required = "auser.can_remove_lab_assistant"
    success_message = "%(first_name)s %(last_name)s successfully removed from lab assistant list."
    success_url = reverse_lazy("auser:all_lab_assistants_list")
    http_method_names = ["post"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="lab assistant") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def form_valid(self, form):
        form.cleaned_data.update({"first_name": self.object.first_name, "last_name": self.object.last_name})
        self.object.groups.remove(Group.objects.get(name="lab assistant"))
        return super().form_valid(form)


class RemoveFromLabAssistantView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Remove user form lab assistant from specifict department lab assistant list."""

    model = UserModel
    fields = ("groups",)
    permission_required = "auser.can_remove_lab_assistant"
    success_message = "%(first_name)s %(last_name)s successfully removed from heads."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("auser:lab_assistants_list", args=[self.kwargs["short_name"]])

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="lab assistant") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def form_valid(self, form):
        form.cleaned_data.update({"first_name": self.object.first_name, "last_name": self.object.last_name})
        self.object.groups.remove(Group.objects.get(name="lab assistant"))
        return super().form_valid(form)


class AllLabAssistantDeleteView(PermissionRequiredMixin, DeleteView):
    """Delete lab assistant from the system."""

    model = UserModel
    permission_required = "auser.can_delete_lab_assistant"
    success_url = reverse_lazy("auser:all_lab_assistants_list")
    http_method_names = ["post"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="lab assistant") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request,
                f" {self.object.get_full_name()} deleted successfully.",
            )
            return response
        except ProtectedError as error:
            messages.error(
                request,
                f"You cann't delete this lab assistant, because there is {len(error.protected_objects)} "
                "related datas. try to delete related objects first.",
            )
            return HttpResponseRedirect(self.success_url)


class LabAssistantDeleteView(PermissionRequiredMixin, DeleteView):
    """Delete lab assistant from the system, from specific department lab assistant list."""

    model = UserModel
    permission_required = "auser.can_delete_lab_assistant"
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("auser:lab_assistants_list", args=[self.kwargs["short_name"]])

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="lab assistant") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request,
                f"Lab assistant {self.object.get_full_name()} deleted successfully.",
            )
            return response
        except ProtectedError as error:
            messages.error(
                request,
                f"You cann't delete this lab assistant, because there is {len(error.protected_objects)} "
                "related datas. try to delete related objects first.",
            )
            return HttpResponseRedirect(self.success_url)
