from .category import (AddCategoryView, AddSubCategoryView, DeleteCategoryView,
                       DeleteSubCategoryView, ListCategoriesView,
                       ListSubCategoriesView, UpdateCategoryView,
                       UpdateSubCategoryView)
from .shelf import (AddShelfView, DeleteShelfView, ListShelvesView,
                    UpdateShelfView)
from .specification import (AddMeasurmentView, AddSpecificationTypeView,
                            DeleteMeasurmentView, DeleteSpecificationTypeView,
                            ListMeasurmentsView, ListSpecificationTypesView,
                            UpdateMeasurmentView, UpdateSpecificationTypeView)
from .store import (AddStoreView, DeleteStoreView, ListStoresView,
                    UpdateStoreView)

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
    "ListMeasurmentsView" "UpdateMeasurmentView",
    "DeleteMeasurmentView",
]
