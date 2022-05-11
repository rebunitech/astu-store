from django.contrib.admin.models import LogEntry
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from auser.mixins import (LogEntryAdditionMixin, LogEntryChangeMixin,
                          LogEntryDeletionMixin)
from auser.models import DepartmentHead
from auser.utils import generate_username


class ListActiveDepartmentsView(PermissionRequiredMixin, ListView):
    """Generic view used to list all content creators"""

    model = DepartmentHead
    permission_required = ("auser.view_department", "auser.add_departmenthead")
    template_name = "auser/content_creator/list_active_content_creator.html"
    context_object_name = "content_creators"
    paginate_by = 10
    extra_context = {"title": _("Active content creators")}

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class ListDeactivatedDepartmentHeadsView(PermissionRequiredMixin, ListView):
    """Generic view used to list all content creators"""

    model = DepartmentHead
    permission_required = ("auser.view_departmenthead", "auser.add_departmenthead")
    template_name = "auser/content_creator/list_deactivated_content_creator.html"
    context_object_name = "deactivated_content_creators"
    paginate_by = 10
    extra_context = {"title": _("Deactivated content creators")}

    def get_queryset(self):
        return self.model.objects.filter(is_active=False)


class AddDepartmentHeadView(
    PermissionRequiredMixin, SuccessMessageMixin, LogEntryAdditionMixin, CreateView
):
    """Generic view used to add content creator"""

    model = DepartmentHead
    fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "sex",
        "location",
        "po_box",
    )
    permission_required = ("auser.add_departmenthead",)
    success_url = reverse_lazy("auser:active_department_head_list")
    success_message = _("%(first_name)s %(last_name)s added successfully")
    template_name = "auser/content_creator/add_content_creator.html"
    extra_context = {"title": _("Add Content Creator")}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = generate_username()
        self.object.save()
        return super().form_valid(form)


class DeactivateDepartmentHeadView(
    PermissionRequiredMixin, SuccessMessageMixin, LogEntryChangeMixin, UpdateView
):
    """Generic view used to deactivate content creator"""

    model = DepartmentHead
    fields = ("is_active",)
    permission_required = ("auser.deactivate_content_creator",)
    success_url = reverse_lazy("auser:active_content_creator_list")
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


class UpdateDepartmentHeadView(
    PermissionRequiredMixin, SuccessMessageMixin, LogEntryChangeMixin, UpdateView
):
    """Generic view used to update content creator"""

    model = DepartmentHead
    fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "sex",
        "location",
        "po_box",
        "profile_picture",
        "bio",
    )
    permission_required = ("auser.change_departmenthead",)
    success_url = reverse_lazy("auser:active_content_creator_list")
    template_name = "auser/content_creator/update_content_creator.html"
    success_message = _("%(first_name)s %(last_name)s updated successfully")
    extra_context = {"title": _("Update Content Creator")}

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class ActivateDepartmentheadView(
    PermissionRequiredMixin, SuccessMessageMixin, LogEntryChangeMixin, UpdateView
):
    """Generic view used to activate content creator"""

    model = DepartmentHead
    fields = ("is_active",)
    permission_required = ("auser.activate_departmenthead",)
    success_url = reverse_lazy("auser:active_content_creator_list")
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


class DeleteDepartmentHead(PermissionRequiredMixin, LogEntryDeletionMixin, DeleteView):
    """Generic view used to delete content creator"""

    model = DepartmentHead
    permission_required = ("auser.delete_departmenthead",)
    success_url = reverse_lazy("auser:deactivated_content_creator_list")
    http_method_names = ["post"]

    def get_queryset(self):
        return self.model.objects.filter(is_active=False)


class DepartmentHeadDetailView(PermissionRequiredMixin, DetailView):
    model = DepartmentHead
    template_name = "auser/content_creator/content_creator_detail.html"
    extra_context = {"title": _("Content Creator Detail")}
    permission_required = ("auser.view_departmenthead", "auser.add_departmenthead")
    context_object_name = "department_head"

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
