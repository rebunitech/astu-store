from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import F, Q, Sum
from django.db.models.functions import Coalesce
from django.views.generic import ListView

from inventory.models import Product


class ListAvailableProductsView(PermissionRequiredMixin, ListView):
    model = Product
    context_object_name = "products"
    permission_required = "view_product"
    extra_context = {"title": "Available Products"}
    template_name = "core/product_list.html"

    # def get_queryset(self):
    #     qs = (
    #         super()
    #         .get_queryset()
    #         .annotate(
    #             total_item=Coalesce(Sum("items__quantity"), 0),
    #             total_request=Coalesce(
    #                 Sum(
    #                     "borrow_requests__quantity",
    #                     filter=Q(borrow_requests__status=1),
    #                 ),
    #                 0,
    #             ),
    #         )
    #         .annotate(total_availables=F("total_item") - F("total_request"))
    #         # .filter(Q(total_availables__gt=0))
    #     )
    #     return qs
