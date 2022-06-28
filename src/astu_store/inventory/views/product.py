from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from inventory.forms import ProductForm
from inventory.models import Product


class AddProductView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = Product
    template_name = "inventory/product/add.html"
    success_url = reverse_lazy("inventory:products_list")
    permission_required = ("inventory.add_product",)
    success_message = _("Product '%(name)s' is successfully added!")
    extra_context = {"title": _("Add Product")}