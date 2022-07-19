from django.urls import include, re_path

from astu_inventory.apps.inventory import views

app_name = "inventory"

urlpatterns = [
    re_path(
        r"^store/",
        include(
            [
                re_path(r"^$", views.ListStoresView.as_view(), name="stores_list"),
                re_path(
                    r"^add/$",
                    views.AddStoreView.as_view(),
                    name="add_store",
                ),
                re_path(
                    r"^(?P<pk>\d+)/",
                    include(
                        [
                            re_path(
                                r"^update/$",
                                views.UpdateStoreView.as_view(),
                                name="update_store",
                            ),
                            re_path(
                                r"^delete/$",
                                views.DeleteStoreView.as_view(),
                                name="delete_store",
                            ),
                            re_path(
                                r"^shelf/",
                                include(
                                    [
                                        re_path(
                                            r"^$",
                                            views.ListShelvesView.as_view(),
                                            name="shelves_list",
                                        ),
                                        re_path(
                                            r"^add/$",
                                            views.AddShelfView.as_view(),
                                            name="add_shelf",
                                        ),
                                        re_path(
                                            r"^(?P<shelf_id>[a-z0-9_\-]+)/",
                                            include(
                                                [
                                                    re_path(
                                                        r"^update/",
                                                        views.UpdateShelfView.as_view(),
                                                        name="update_shelf",
                                                    ),
                                                    re_path(
                                                        r"^delete/$",
                                                        views.DeleteShelfView.as_view(),
                                                        name="delete_shelf",
                                                    ),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    re_path(
        r"^specification/",
        include(
            [
                re_path(
                    r"^type/",
                    include(
                        [
                            re_path(
                                r"^$",
                                views.ListSpecificationTypesView.as_view(),
                                name="specification_types_list",
                            ),
                            re_path(
                                r"^add/$",
                                views.AddSpecificationTypeView.as_view(),
                                name="add_specification_type",
                            ),
                            re_path(
                                r"^(?P<pk>\d+)/",
                                include(
                                    [
                                        re_path(
                                            r"^update/$",
                                            views.UpdateSpecificationTypeView.as_view(),
                                            name="update_specification_type",
                                        ),
                                        re_path(
                                            r"^delete/$",
                                            views.DeleteSpecificationTypeView.as_view(),
                                            name="delete_specification_type",
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                )
            ]
        ),
    ),
    re_path(
        r"^category/",
        include(
            [
                re_path(
                    r"^$",
                    views.ListCategoriesView.as_view(),
                    name="categories_list",
                ),
                re_path(r"^add/$", views.AddCategoryView.as_view(), name="add_category"),
                re_path(
                    r"^(?P<slug>[-a-zA-Z0-9_]+)/",
                    include(
                        [
                            re_path(
                                r"^update/$",
                                views.UpdateCategoryView.as_view(),
                                name="update_category",
                            ),
                            re_path(
                                r"^delete/$",
                                views.DeleteCategoryView.as_view(),
                                name="delete_category",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    re_path(
        r"^subcategory/",
        include(
            [
                re_path(
                    r"^$",
                    views.ListSubCategoriesView.as_view(),
                    name="sub_categories_list",
                ),
                re_path(
                    r"^add/$",
                    views.AddSubCategoryView.as_view(),
                    name="add_sub_category",
                ),
                re_path(
                    r"^(?P<slug>[-a-zA-Z0-9_]+)/",
                    include(
                        [
                            re_path(
                                r"^update/$",
                                views.UpdateSubCategoryView.as_view(),
                                name="update_sub_category",
                            ),
                            re_path(
                                r"^delete/$",
                                views.DeleteSubCategoryView.as_view(),
                                name="delete_sub_category",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    re_path(
        r"^measurment/",
        include(
            [
                re_path(
                    r"^$",
                    views.ListMeasurmentsView.as_view(),
                    name="measurments_list",
                ),
                re_path(r"^add/$", views.AddMeasurmentView.as_view(), name="add_measurment"),
                re_path(
                    r"^(?P<pk>\d+)/",
                    include(
                        [
                            re_path(
                                r"^update/$",
                                views.UpdateMeasurmentView.as_view(),
                                name="update_measurment",
                            ),
                            re_path(
                                r"^delete/$",
                                views.DeleteMeasurmentView.as_view(),
                                name="delete_measurment",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    re_path(
        r"^product/",
        include(
            [
                re_path(r"^$", views.ListProductsView.as_view(), name="products_list"),
                re_path(r"^add/$", views.AddProductView.as_view(), name="add_product"),
                re_path(r"^import/products/$", views.ImportProductsView.as_view(), name="import_products"),
                re_path(
                    r"^(?P<short_name>[a-zA-Z0-9\_\-]+)/(?P<slug>[-a-zA-Z0-9_]+)/",
                    include(
                        [
                            re_path(
                                r"^update/$",
                                views.UpdateProductView.as_view(),
                                name="update_product",
                            ),
                            re_path(
                                r"^delete/$",
                                views.DeleteProductView.as_view(),
                                name="delete_product",
                            ),
                            re_path(
                                r"^specification/",
                                include(
                                    [
                                        re_path(
                                            r"^$",
                                            views.ListProductSpecificationsView.as_view(),
                                            name="product_specifications_list",
                                        ),
                                        re_path(
                                            r"^add/$",
                                            views.AddProductSpecificationView.as_view(),
                                            name="add_product_specification",
                                        ),
                                        re_path(
                                            r"^(?P<s_pk>\d+)/",
                                            include(
                                                [
                                                    re_path(
                                                        r"^update/$",
                                                        views.UpdateProductSpecificationView.as_view(),
                                                        name="update_product_specification",
                                                    ),
                                                    re_path(
                                                        r"^delete/$",
                                                        views.DeleteProductSpecificationView.as_view(),
                                                        name="delete_product_specification",
                                                    ),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            re_path(
                                r"^image/",
                                include(
                                    [
                                        re_path(
                                            r"^$",
                                            views.ListProductImageView.as_view(),
                                            name="product_image_list",
                                        ),
                                        re_path(
                                            r"^add/$",
                                            views.AddProductImageView.as_view(),
                                            name="add_product_image",
                                        ),
                                        re_path(
                                            r"^(?P<img_pk>\d+)/",
                                            include(
                                                [
                                                    re_path(
                                                        r"^delete/$",
                                                        views.DeleteProductImageView.as_view(),
                                                        name="delete_product_image",
                                                    ),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    re_path(
        r"^item/",
        include(
            [
                re_path(r"^import/items/$", views.ImportItemsView.as_view(), name="import_items"),
                re_path(r"^$", views.ListItemsView.as_view(), name="items_list"),
                re_path(
                    r"^add/$",
                    views.AddItemView.as_view(),
                    name="add_item",
                ),
                re_path(
                    r"^(?P<pk>\d+)/",
                    include(
                        [
                            re_path(
                                r"^update/$",
                                views.UpdateItemView.as_view(),
                                name="update_item",
                            ),
                            re_path(
                                r"^delete/$",
                                views.DeleteItemView.as_view(),
                                name="delete_item",
                            ),
                            re_path(
                                r"^specification/",
                                include(
                                    [
                                        re_path(
                                            r"^$",
                                            views.ListItemSpecificationsView.as_view(),
                                            name="item_specifications_list",
                                        ),
                                        re_path(
                                            r"^add/$",
                                            views.AddItemSpecificationView.as_view(),
                                            name="add_item_specification",
                                        ),
                                        re_path(
                                            r"^(?P<s_pk>\d+)/",
                                            include(
                                                [
                                                    re_path(
                                                        r"^update/$",
                                                        views.UpdateItemSpecificationView.as_view(),
                                                        name="update_item_specification",
                                                    ),
                                                    re_path(
                                                        r"^delete/$",
                                                        views.DeleteItemSpecificationView.as_view(),
                                                        name="delete_item_specification",
                                                    ),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    re_path(
        r"^lab/",  # TODO:
        include(
            [
                re_path(r"^$", views.ListLabsView.as_view(), name="labs_list"),
                re_path(
                    r"^add/$",
                    views.AddLabView.as_view(),
                    name="add_lab",
                ),
                re_path(
                    r"^(?P<pk>\d+)/",
                    include(
                        [
                            re_path(
                                r"^update/$",
                                views.UpdateLabView.as_view(),
                                name="update_lab",
                            ),
                            re_path(
                                r"^delete/$",
                                views.DeleteLabView.as_view(),
                                name="delete_lab",
                            ),
                            re_path(
                                r"^table/",
                                include(
                                    [
                                        re_path(
                                            r"^$",
                                            views.ListTablesView.as_view(),
                                            name="tables_list",
                                        ),
                                        re_path(
                                            r"^add/$",
                                            views.AddTableView.as_view(),
                                            name="add_table",
                                        ),
                                        re_path(
                                            r"^(?P<table_id>[a-z0-9_\-]+)/",
                                            include(
                                                [
                                                    re_path(
                                                        r"^update/",
                                                        views.UpdateTableView.as_view(),
                                                        name="update_table",
                                                    ),
                                                    re_path(
                                                        r"^delete/$",
                                                        views.DeleteTableView.as_view(),
                                                        name="delete_table",
                                                    ),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
]
