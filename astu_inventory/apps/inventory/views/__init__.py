from .category import (
    AddCategoryView,
    AddSubCategoryView,
    DeleteCategoryView,
    DeleteSubCategoryView,
    ListCategoriesView,
    ListSubCategoriesView,
    UpdateCategoryView,
    UpdateSubCategoryView,
)
from .item import AddItemView, DeleteItemView, ImportItemsView, ListItemsView, UpdateItemView
from .lab import AddLabView, DeleteLabView, ListLabsView, UpdateLabView
from .product import AddProductView, DeleteProductView, ImportProductsView, ListProductsView, UpdateProductView
from .shelf import AddShelfView, DeleteShelfView, ListShelvesView, UpdateShelfView
from .specification import (
    AddItemSpecificationView,
    AddMeasurmentView,
    AddProductSpecificationView,
    AddSpecificationTypeView,
    DeleteItemSpecificationView,
    DeleteMeasurmentView,
    DeleteProductSpecificationView,
    DeleteSpecificationTypeView,
    ListItemSpecificationsView,
    ListMeasurmentsView,
    ListProductSpecificationsView,
    ListSpecificationTypesView,
    UpdateItemSpecificationView,
    UpdateMeasurmentView,
    UpdateProductSpecificationView,
    UpdateSpecificationTypeView,
)
from .store import AddStoreView, DeleteStoreView, ListStoresView, UpdateStoreView
from .table import AddTableView, DeleteTableView, ListTablesView, UpdateTableView

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
    "AddLabView",
    "ListLabsView",
    "UpdateLabView",
    "DeleteLabView",
    # Table,
    "AddTableView",
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
    "ListCategoriesView",
    "UpdateCategoryView",
    "DeleteCategoryView",
    # Sub Category
    "AddSubCategoryView",
    "ListSubCategoriesView",
    "UpdateSubCategoryView",
    "DeleteSubCategoryView",
    # Measurment
    "AddMeasurmentView",
    "ListMeasurmentsView",
    "UpdateMeasurmentView",
    "DeleteMeasurmentView",
    # Product
    "AddProductView",
    "ImportProductsView",
    "ListProductsView",
    "UpdateProductView",
    "DeleteProductView",
    # Item
    "AddItemView",
    "ImportItemsView",
    "ListItemsView",
    "UpdateItemView",
    "DeleteItemView",
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
