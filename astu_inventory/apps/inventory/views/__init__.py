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
from .lab import AddLabView, DeleteLabView, ListLabsView, SpecificLabListView, UpdateLabView
from .product import (
    AddProductImageView,
    AddProductView,
    DeleteProductImageView,
    DeleteProductView,
    ImportProductsView,
    ListProductImageView,
    ListProductsView,
    UpdateProductView,
)
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
from .store import AddStoreView, DeleteStoreView, ListStoresView, SpecificListStoreView, UpdateStoreView
from .table import AddTableView, DeleteTableView, ListTablesView, UpdateTableView

__all__ = [
    # Store
    "AddStoreView",
    "ListStoresView",
    "UpdateStoreView",
    "DeleteStoreView",
    "SpecificListStoreView",
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
    "SpecificLabListView",
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
    "AddProductImageView",
    # Product
    "AddProductView",
    "ImportProductsView",
    "ListProductsView",
    "UpdateProductView",
    "DeleteProductView",
    "ListProductImageView",
    "DeleteProductImageView",
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
