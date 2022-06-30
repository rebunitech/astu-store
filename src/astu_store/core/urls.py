from django.urls import include, re_path

from core import views

app_name = "core"

urlpatterns = [
    re_path(
        r"^products",
        views.ListAvailableProductsView.as_view(),
        name="available_products_list",
    ),
    re_path(
        r"^product/(?P<slug>[-a-zA-Z0-9_]+)/borrow/request/",
        include(
            [
                re_path(
                    r"^$",
                    views.InitiateBorrowRequestView.as_view(),
                    name="initiate_borrow_request",
                ),
            ]
        ),
    ),
]
