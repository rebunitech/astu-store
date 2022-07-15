from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from astu_inventory.apps.inventory.forms import ItemForm
from astu_inventory.apps.inventory.models import Item


class AddItemView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = "inventory/item/add.html"
    success_url = reverse_lazy("inventory:items_list")
    permission_required = "inventory.add_item"
    success_message = _("Item is successfully added!")
    extra_context = {"title": _("Add Item")}

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        user = self.request.user
        if user.is_superuser or user.is_college_dean:
            return form
        form["product"].field.queryset = form["user"].field.queryset.filter(department=user.department)
        return form


class ListItemsView(PermissionRequiredMixin, ListView):
    model = Item
    context_object_name = "items"
    permission_required = "inventory.view_item"
    extra_context = {"title": _("Items")}
    template_name = "inventory/item/list.html"

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.is_college_dean:
            return qs
        if user.is_department_head:
            return qs.filter(Q(store__department=user.department))
        return qs.filter(Q(store__store_officers__pk=user.pk))


class UpdateItemView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = "inventory/item/update.html"
    success_url = reverse_lazy("inventory:items_list")
    permission_required = "inventory.change_item"
    success_message = _("Item is updated successfully!")
    extra_context = {"title": _("Update Item")}

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.is_college_dean:
            return qs
        if user.is_department_head:
            return qs.filter(Q(store__department=user.department))
        return qs.filter(Q(store__store_officers__pk=user.pk))


class DeleteItemView(PermissionRequiredMixin, DeleteView):
    model = Item
    permission_required = "inventory.delete_item"
    http_method_names = ["post"]
    success_url = reverse_lazy("inventory:items_list")

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.is_college_dean:
            return qs
        if user.is_department_head:
            return qs.filter(Q(store__department=user.department))
        return qs.filter(Q(store__store_officers__pk=user.pk))
