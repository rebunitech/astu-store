from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from astu_inventory.apps.inventory.forms import AddProductForm, AddProductImageForm, UpdateProductForm
from astu_inventory.apps.inventory.models import Product, ProductImage


class AddProductView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = AddProductForm
    template_name = "inventory/product/add.html"
    success_url = reverse_lazy("inventory:products_list")
    permission_required = "inventory.add_product"
    success_message = _("Product '%(name)s' is successfully added!")
    extra_context = {"title": _("Add Product")}


class UpdateProductView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = UpdateProductForm
    template_name = "inventory/product/update.html"
    success_url = reverse_lazy("inventory:products_list")
    permission_required = "inventory.change_product"
    success_message = _("Product '%(name)s' is updated successfully!")
    extra_context = {"title": _("Update Product")}

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset().filter(department__short_name__iexact=self.kwargs["short_name"])
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(department=user.department)


class ListProductsView(PermissionRequiredMixin, ListView):
    model = Product
    context_object_name = "products"
    permission_required = "inventory.view_product"
    extra_context = {"title": _("Products")}
    template_name = "inventory/product/list.html"

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(Q(department=user.department))


class DeleteProductView(PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = "inventory.delete_product"
    http_method_names = ["post"]
    success_url = reverse_lazy("inventory:products_list")

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset().filter(department__short_name__iexact=self.kwargs["short_name"])
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(Q(department=user.department))


class AddProductImageView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ProductImage
    form_class = AddProductImageForm
    permission_required = ("inventory.add_image",)
    success_message = _("Image added successfully.")
    template_name = "inventory/product/image/add.html"
    context_object_name = "images"
    extra_context = {"title": _("Add Image")}

    def get_initial(self):
        return self.kwargs

    def get_success_url(self):
        return reverse_lazy(
            "inventory:product_image_list",
            kwargs=self.kwargs,
        )


class ListProductImageView(PermissionRequiredMixin, ListView):
    model = ProductImage
    permission_required = ("inventory.view_image",)
    context_object_name = "images"
    template_name = "inventory/product/image/list.html"
    extra_context = {"title": _("Product Images")}

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                product__slug=self.kwargs.get("slug"),
                product__department__short_name__iexact=self.kwargs["short_name"],
            )
        )


class DeleteProductImageView(PermissionRequiredMixin, DeleteView):
    model = ProductImage
    permission_required = ("inventory.delete_image",)
    http_method_names = ["post"]
    pk_url_kwarg = "img_pk"

    def get_success_url(self):
        self.kwargs.pop("img_pk")
        return reverse_lazy(
            "inventory:product_image_list",
            kwargs=self.kwargs,
        )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                product__slug=self.kwargs.get("slug"),
                product__department__short_name__iexact=self.kwargs["short_name"],
            )
        )
