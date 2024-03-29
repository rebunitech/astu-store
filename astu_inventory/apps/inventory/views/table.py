from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from astu_inventory.apps.inventory.forms import TableForm
from astu_inventory.apps.inventory.models import Lab, Table


class AddTableView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Table
    form_class = TableForm
    permission_required = "inventory.add_table"
    success_message = _("Table added successfully.")
    template_name = "inventory/lab/table/add.html"
    extra_context = {"title": _("Add Table")}

    def get_lab(self):
        return get_object_or_404(Lab, pk=self.kwargs.get("pk"))

    def form_valid(self, form):
        form.instance.lab = self.get_lab()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("inventory:tables_list", kwargs={"pk": self.kwargs.get("pk")})


class ListTablesView(PermissionRequiredMixin, ListView):
    model = Table
    permission_required = ("inventory.view_table",)
    context_object_name = "tables"
    template_name = "inventory/lab/table/list.html"
    extra_context = {"title": _("Tables")}

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset().filter(lab__pk=self.kwargs.get("pk"))
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(Q(lab__department=user.collegeuser.department))


class UpdateTableView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Table
    form_class = TableForm
    permission_required = ("inventory.change_table",)
    success_message = _("Table updated successfully.")
    template_name = "inventory/lab/table/update.html"
    extra_context = {"title": _("Update table")}
    pk_url_kwarg = None
    slug_field = "table_id"
    slug_url_kwarg = "table_id"

    def get_success_url(self):
        return reverse_lazy("inventory:tables_list", kwargs={"pk": self.kwargs.get("pk")})

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs
        qs.filter(lab__pk=self.kwargs.get("pk"))
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(Q(lab__department=user.department))


class DeleteTableView(PermissionRequiredMixin, DeleteView):
    model = Table
    permission_required = "inventory.delete_table"
    pk_url_kwarg = None
    slug_field = "table_id"
    slug_url_kwarg = "table_id"
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("inventory:tables_list", kwargs={"pk": self.kwargs.get("pk")})

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset().filter(lab__pk=self.kwargs.get("pk"))
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(Q(lab__department=user.department))
