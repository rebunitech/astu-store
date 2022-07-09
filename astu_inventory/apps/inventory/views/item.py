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
    permission_required = ("inventory.add_item",)
    success_message = _("Item '%(name)s' is successfully added!")
    extra_context = {"title": _("Add Item")}


class ListItemsView(PermissionRequiredMixin, ListView):
    model = Item
    context_object_name = "items"
    permission_required = "inventory.view_item"
    extra_context = {"title": _("Items")}
    template_name = "inventory/item/list.html"

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if not user.is_college_user:
            return qs
        if user.is_college_representative:
            return qs.filter(Q(store__department__college=user.collegeuser.college))
        if user.is_department_representative:
            return qs.filter(Q(store__department=user.collegeuser.department))
        if user.is_store_officer:
            return qs.filter(Q(store__store_officers__pk=user.pk))
        return qs.filter(Q(id=None))


class UpdateItemView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = "inventory/item/update.html"
    success_url = reverse_lazy("inventory:items_list")
    permission_required = ("inventory.change_item",)
    success_message = _("Item '%(name)s' is updated successfully!")
    extra_context = {"title": _("Update Item")}

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if not user.is_college_user:
            return qs
        if user.is_college_representative:
            return qs.filter(Q(store__department__college=user.collegeuser.college))
        if user.is_department_representative:
            return qs.filter(Q(store__department=user.collegeuser.department))
        if user.is_store_officer:
            return qs.filter(Q(store__store_officers__pk=user.pk))
        return qs.filter(Q(id=None))


class DeleteItemView(PermissionRequiredMixin, DeleteView):
    model = Item
    permission_required = ("inventory.delete_item",)
    http_method_names = ["post"]
    success_url = reverse_lazy("inventory:items_list")

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if not user.is_college_user:
            return qs
        if user.is_college_representative:
            return qs.filter(Q(store__department__college=user.collegeuser.college))
        if user.is_department_representative:
            return qs.filter(Q(store__department=user.collegeuser.department))
        if user.is_store_officer:
            return qs.filter(Q(store__store_officers__pk=user.pk))
        return qs.filter(Q(id=None))
