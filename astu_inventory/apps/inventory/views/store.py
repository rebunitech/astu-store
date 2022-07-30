from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from astu_inventory.apps.auser.models import Department
from astu_inventory.apps.inventory.models import Store


class AddStoreView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """Add store to the system (all list of store)"""

    model = Store
    fields = ("department", "block", "room", "remark")
    permission_required = "inventory.add_store"
    success_message = _("Store added successfully.")
    template_name = "inventory/store/add.html"
    success_url = reverse_lazy("inventory:stores_list")
    extra_context = {"title": _("Add store")}

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        user = self.request.user
        if user.is_superuser or user.is_college_dean:
            return form
        form["department"].field.queryset = user.department
        return form


class ListStoresView(PermissionRequiredMixin, ListView):
    model = Store
    permission_required = "inventory.can_list_stores"
    context_object_name = "stores"
    template_name = "inventory/store/list.html"
    extra_context = {"title": _("Stores")}

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(Q(department=user.department))


class SpecificListStoreView(PermissionRequiredMixin, SuccessMessageMixin, ListView):
    """List stores for specific department."""

    model = Store
    permission_required = "inventory.can_list_stores"
    template_name = "inventory/store/specific/list.html"
    context_object_name = "stores"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"{self.kwargs['short_name'].upper()} stores."})
        return context_data

    def get_queryset(self):
        return super().get_queryset().filter(Q(department__short_name__iexact=self.kwargs["short_name"]))


class UpdateStoreView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Store
    fields = ("block", "room", "status", "remark")
    permission_required = "inventory.change_store"
    success_message = _("Store updated successfully.")
    template_name = "inventory/store/update.html"
    success_url = reverse_lazy("inventory:stores_list")
    extra_context = {"title": _("Update store")}

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(Q(department=user.department))


class DeleteStoreView(PermissionRequiredMixin, DeleteView):
    model = Store
    permission_required = ("store.delete_store",)
    success_url = reverse_lazy("inventory:stores_list")
    http_method_names = ["post"]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(Q(department=user.department))
