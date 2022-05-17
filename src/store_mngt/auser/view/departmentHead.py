from django.contrib.admin.models import LogEntry
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from auser.models import DepartmentHead

from auser.utils import generate_username


class AddDepartmenHead(CreateView, SuccessMessageMixin, PermissionRequiredMixin):
    """Generic view used to add department head"""

    model = DepartmentHead
    fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "sex",
        "location",
        "po_box",
        "department",
    )
    permission_required = ("auser.add_department_head",)  #TODO:
    template_name = "auser/departmentHead/add_department_head.html"
    success_message = _("%(first_name)s %(last_name)s added successfully")
    success_url = reverse_lazy("auser:active_department_head_list")
    extra_context = {"title": _("Add Department Head")}
    def form_valid(self, form):
            self.object = form.save(commit=False)
            self.object.username = generate_username()
            self.object.save()
            return super().form_valid(form)

class UpdateDepartmentHead( PermissionRequiredMixin, 
                            SuccessMessageMixin, UpdateView 
                            ):
    """Generic view used to update department head"""

    model = DepartmentHead
    fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "department",
        "sex",
        "location",
        "po_box",
        "profile_picture",
        "bio",
    )
    permission_required = ("auser.change_department_head",)
    success_url = reverse_lazy("auser:active_department_head_list")
    template_name = "auser/departmentHead/update_department_head.html"
    success_message = _("%(first_name)s %(last_name)s updated successfully")
    extra_context = {"title": _("Update Department Head")}

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class ListActiveDepartmentHeadsView(PermissionRequiredMixin, ListView):
    """Generic view used to list all Department heads"""

    model = DepartmentHead
    permission_required = ("auser.view_department_head", "auser.add_department_head")
    template_name = "auser/departmentHead/list_active_department_head.html"
    context_object_name = "department_heads"
    paginate_by = 10
    extra_context = {"title": _("Active department heads")}

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class ListDeactivatedDepartmentHeadsView(PermissionRequiredMixin, ListView):
    """Generic view used to list all Department heads"""

    model = DepartmentHead
    permission_required = ("auser.view_department_head", "auser.add_department_head")
    template_name = "auser/departmentHead/list_deactivated_department_head.html"
    context_object_name = "deactivated_department_heads"
    paginate_by = 10
    extra_context = {"title": _("Deactivated department heads")}

    def get_queryset(self):
        return self.model.objects.filter(is_active=False)


class DeactivateDepartmentHeadView(
                                     PermissionRequiredMixin, 
                                     SuccessMessageMixin, UpdateView
                                    ):
    """Generic view used to deactivate department head"""

    model = DepartmentHead
    fields = ("is_active",)
    permission_required = ("auser.deactivate_department_head",)
    success_url = reverse_lazy("auser:active_department_head_list")
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


class ActivateDepartmentHeadView(
                                  PermissionRequiredMixin, 
                                  SuccessMessageMixin, UpdateView 
                                  ):
    """Generic view used to activate department head"""

    model = DepartmentHead
    fields = ("is_active",)
    permission_required = ("auser.activate_department_head",)
    # success_url = reverse_lazy("auser:active_department_head_list")
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


class DeleteDepartmentHead(PermissionRequiredMixin, DeleteView):
    """Generic view used to delete department head. """

    model = DepartmentHead
    permission_required = ("auser.delete_departmenthead",)
    success_url = reverse_lazy("auser:deactivated_department_head_list")
    http_method_names = ["post"]

    def get_queryset(self):
        return self.model.objects.filter(is_active=False)


class DepartmentHeadDetailView(PermissionRequiredMixin, DetailView):
    model = DepartmentHead
    template_name = "auser/departmentHead/department_head_detail.html"
    extra_context = {"title": _("Department Head Detail")}
    permission_required = ("auser.view_department_head", "auser.add_department_head")
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
