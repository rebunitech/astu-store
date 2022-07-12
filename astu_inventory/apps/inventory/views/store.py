from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from astu_inventory.apps.auser.models import Department
from astu_inventory.apps.inventory.models import Store


class AddStoreView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
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
        form["department"].field.queryset = Department.objects.filter(
            Q(department=user.department)
        )
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
