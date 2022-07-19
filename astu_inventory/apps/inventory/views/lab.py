from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from astu_inventory.apps.auser.models import Department
from astu_inventory.apps.inventory.models import Lab


class AddLabView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Lab
    fields = ("department", "block", "room", "remark")
    permission_required = "inventory.add_lab"
    success_message = _("Lab added successfully.")
    template_name = "inventory/lab/add.html"
    success_url = reverse_lazy("inventory:labs_list")
    extra_context = {"title": _("Add lab")}

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        user = self.request.user
        if user.is_superuser or user.is_college_dean:
            return form
        form["department"].field.queryset = Department.objects.filter(Q(department=user.department))
        return form


class ListLabsView(PermissionRequiredMixin, ListView):
    model = Lab
    permission_required = "inventory.view_lab"
    context_object_name = "labs"
    template_name = "inventory/lab/list.html"
    extra_context = {"title": _("Labs")}

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(Q(department=user.department))


class SpecificLabListView(PermissionRequiredMixin, ListView):
    """List of labs for specific department."""

    model = Lab
    permission_required = "inventory.view_lab"
    context_object_name = "labs"
    template_name = "inventory/lab/specific/list.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data.update({"title": f"{self.kwargs['short_name'].upper()} labs"})
        return context_data

    def get_queryset(self):
        return super().get_queryset().filter(Q(department__short_name__iexact=self.kwargs["short_name"]))


class UpdateLabView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Lab
    fields = ("block", "room", "status", "remark")
    permission_required = "inventory.change_lab"
    success_message = _("Lab updated successfully.")
    template_name = "inventory/lab/update.html"
    success_url = reverse_lazy("inventory:labs_list")
    extra_context = {"title": _("Update lab")}

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(Q(department=user.department))


class DeleteLabView(PermissionRequiredMixin, DeleteView):
    model = Lab
    permission_required = "inventory.delete_lab"
    success_url = reverse_lazy("inventory:labs_list")
    http_method_names = ["post"]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(Q(department=user.department))
