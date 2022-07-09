from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from astu_inventory.apps.inventory.forms import ProductForm
from astu_inventory.apps.inventory.models import Product


class AddProductView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "inventory/product/add.html"
    success_url = reverse_lazy("inventory:products_list")
    permission_required = ("inventory.add_product",)
    success_message = _("Product '%(name)s' is successfully added!")
    extra_context = {"title": _("Add Product")}


class UpdateProductView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "inventory/product/update.html"
    success_url = reverse_lazy("inventory:products_list")
    permission_required = ("inventory.change_product",)
    success_message = _("Product '%(name)s' is updated successfully!")
    extra_context = {"title": _("Update Product")}

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if not user.is_college_user:
            return qs
        if user.is_college_representative:
            return qs.filter(Q(college=user.collegeuser.college))
        return qs.filter(Q(department=user.collegeuser.department))


class ListProductsView(PermissionRequiredMixin, ListView):
    model = Product
    context_object_name = "products"
    permission_required = "inventory.view_product"
    extra_context = {"title": _("Products")}
    template_name = "inventory/product/list.html"

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if not user.is_college_user:
            return qs
        if user.is_college_representative:
            return qs.filter(Q(college=user.collegeuser.college))
        return qs.filter(Q(department=user.collegeuser.department))


class DeleteProductView(PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = ("inventory.delete_product",)
    http_method_names = ["post"]
    success_url = reverse_lazy("inventory:products_list")

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if not user.is_college_user:
            return qs
        if user.is_college_representative:
            return qs.filter(Q(college=user.collegeuser.college))
        return qs.filter(Q(department=user.collegeuser.department))
