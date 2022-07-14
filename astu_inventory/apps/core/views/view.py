from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import F, Q, Sum
from django.db.models.functions import Coalesce
from django.views.generic import ListView

from astu_inventory.apps.inventory.models import Product


class ListAvailableProductsView(PermissionRequiredMixin, ListView):
    model = Product
    context_object_name = "products"
    permission_required = "core.can_list_available_product"
    extra_context = {"title": "Products"}
    template_name = "core/product_list.html"
