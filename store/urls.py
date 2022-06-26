from django.urls import include, re_path

from store import views

app_name = "store"

store_urls = [
    re_path(r"^$", views.ListStoresView.as_view(), name="list_stores"),
    re_path(r"^add/$", views.AddStoreView.as_view(), name="add_store"),
    re_path(r"^(?P<pk>\d+)/update/$", views.UpdateStoreView.as_view(), name="update_store"),
    re_path(
        r"^(?P<pk>\d+)/delete/$", views.DeleteStoreView.as_view(), name="delete_store"
    ),
]

shellf_urls = [
    re_path(
        r"^(?P<store_pk>\d+)/$", views.ListShelvesView.as_view(), name="list_shelves"
    ),
    re_path(
        r"^add/(?P<store_pk>\d+)/$", views.AddShelfView.as_view(), name="add_shelf"
    ),
    re_path(
        r"^(?P<uuid>[-a-zA-Z0-9_]+)/update/$",
        views.UpdateShelfView.as_view(),
        name="update_shelf",
    ),
    re_path(
        r"^(?P<uuid>[-a-zA-Z0-9_]+)/delete/$",
        views.DeleteShelfView.as_view(),
        name="delete_shelf",
    ),
]

item_urls = [
    re_path(r"^$", views.ListItemsView.as_view(), name="list_items"),
    re_path(r"^add/$", views.AddItemView.as_view(), name="add_item"),
    re_path(r"^(?P<pk>\d+)/update/$", views.UpdateItemView.as_view(), name="update_item"),
    re_path(
        r"^(?P<pk>\d+)/delete/$", views.DeleteItemView.as_view(), name="delete_item"
    ),
]

specification_urls = [
    re_path(
        r"^(?P<item_pk>\d+)/$",
        views.ListSpecificationsView.as_view(),
        name="list_specifications",
    ),
    re_path(
        r"^add/(?P<item_pk>\d+)/$",
        views.AddSpecificationView.as_view(),
        name="add_specification",
    ),
    re_path(
        r"^(?P<pk>\d+)/update/$",
        views.UpdateSpecificationView.as_view(),
        name="update_specification",
    ),
    re_path(
        r"^(?P<pk>\d+)/delete/$",
        views.DeleteSpecificationView.as_view(),
        name="delete_specification",
    ),
]

specification_type_urls = [
    re_path(
        r"^add/$",
        views.AddSpecificationTypeView.as_view(),
        name="add_specification_type",
    ),
    re_path(
        r"^list/$",
        views.ListSpecificationTypesView.as_view(),
        name="list_specification_types",
    ),
    re_path(
        r"^(?P<pk>\d+)/$",
        views.UpdateSpecificationTypeView.as_view(),
        name="update_specification_type",
    ),
    re_path(
        r"^delete/(?P<pk>\d+)/$",
        views.DeleteSpecificationTypeView.as_view(),
        name="delete_specification_type",
    ),
]

urlpatterns = [
    re_path(r"^stores/", include(store_urls)),
    re_path(r"^shelf/", include(shellf_urls)),
    re_path(r"^items/", include(item_urls)),
    re_path(r"^specifications/", include(specification_urls)),
    re_path(r"^specification/type/", include(specification_type_urls)),
]
