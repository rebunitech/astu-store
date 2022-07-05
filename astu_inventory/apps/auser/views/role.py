"""ASTU Inventory auser views

Each class represents a logic layer of the project, related to roles.

    Date Created: 4 July, 2022
    Author: Wendirad Demelash(@wendirad)
"""

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, UpdateView

from astu_inventory.apps.auser.forms import ChangePermissionForm


class ListRolesView(PermissionRequiredMixin, ListView):
    model = Group
    context_object_name = "roles"
    permission_required = ("auth.view_group",)
    template_name = "auser/role/list.html"
    extra_context = {"title": "Roles"}

    def get_queryset(self):
        return super().get_queryset().values("pk", "name")


class UpdateRoleView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Group
    form_class = ChangePermissionForm
    context_object_name = "role"
    permission_required = ("auth.change_group",)
    template_name = "auser/role/update.html"
    success_url = reverse_lazy("auser:roles_list")
    success_message = _("Role permissions updated successfully.")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": "Update %s permissions" % self.object.name})
        return context_data
