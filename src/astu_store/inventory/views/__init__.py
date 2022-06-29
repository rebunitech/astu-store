from .category import (AddCategoryView, AddSubCategoryView, DeleteCategoryView,
                       DeleteSubCategoryView, ListCategoriesView,
                       ListSubCategoriesView, UpdateCategoryView,
                       UpdateSubCategoryView)
from .product import (AddProductView, DeleteProductView, ListProductsView,
                      UpdateProductView)
from .shelf import (AddShelfView, DeleteShelfView, ListShelvesView,
                    UpdateShelfView)
from .specification import (AddMeasurmentView, AddSpecificationTypeView,
                            DeleteMeasurmentView, DeleteSpecificationTypeView,
                            ListMeasurmentsView, ListSpecificationTypesView,
                            UpdateMeasurmentView, UpdateSpecificationTypeView, AddItemSpecificationView, ListItemSpecificationsView, UpdateItemSpecificationView, DeleteItemSpecificationView,
                            AddProductSpecificationView, ListProductSpecificationsView, UpdateProductSpecificationView, DeleteProductSpecificationView
                            )
from .store import (AddStoreView, DeleteStoreView, ListStoresView,
                    UpdateStoreView)
from .lab import (AddLabView, DeleteLabView, ListLabsView,
                    UpdateLabView)

from .table import (AddTableView, DeleteTableView, ListTablesView,
                    UpdateTableView)
from .item import AddItemView, UpdateItemView, ListItemsView, DeleteItemView


__all__ = [
    # Store
    "AddStoreView",
    "ListStoresView",
    "UpdateStoreView",
    "DeleteStoreView",
    # Shelf
    "AddShelfView",
    "ListShelvesView",
    "UpdateShelfView",
    "DeleteShelfView",
    # Lab
    'AddLabView',
    "ListLabsView",
    "UpdateLabView",
    "DeleteLabView",
    # Table,
    'AddTableView',
    "ListTablesView",
    "UpdateTableView",
    "DeleteTableView",
    # SpecificationType
    "AddSpecificationTypeView",
    "ListSpecificationTypesView",
    "UpdateSpecificationTypeView",
    "DeleteSpecificationTypeView",
    # Category
    "AddCategoryView",
    "ListCategoriesView" "UpdateCategoryView",
    "DeleteCategoryView"
    # Sub Category
    "AddSubCategoryView",
    "ListSubCategoryView",
    "UpdateSubCategoryView",
    "DeleteSubCategoryView",
    # Measurment
    "AddMeasurmentView",
    "ListMeasurmentsView",
    "UpdateMeasurmentView",
    "DeleteMeasurmentView",
    # Product
    "AddProductView",
    "ListProductsView",
    "UpdateProductView",
    "DeleteProductView",
    # Item
    "AddItemView",
    "ListItemsView",
    "UpdateItemView",
    "DeleteItemView"
    # Item Specification
    "AddItemSpecificationView",
    "ListItemSpecificationsView",
    "UpdateItemSpecificationView",
    "DeleteItemSpecificationView",
    # Product Specification
    "AddProductSpecificationView",
    "ListProductSpecificationsView",
    "UpdateProductSpecificationView",
    "DeleteProductSpecificationView",

]
