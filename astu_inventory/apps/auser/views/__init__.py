from .department import (
    ActivateDepartmentView,
    AddDepartmentView,
    AllDepartmentHeadsListView,
    DeactivateDepartmentView,
    DeleteDepartmentView,
    ListDepartmentsView,
    UpdateDepartmentView,
)
from .role import ListRolesView, UpdateRoleView
from .user import (
    AddCollegeDeanView,
    CollegeDeanActivateView,
    CollegeDeanDeactivateView,
    CollegeDeanDeleteView,
    CollegeDeansListView,
    CollegeDeanUpdateView,
    ProfileEditView,
    RemoveFromCollegeDeanView,
    SelectCollegeDeanView,
)

__all__ = [
    # User
    "ProfileEditView",
    # Role
    "ListRolesView",
    "UpdateRoleView",
    # Department
    "ListDepartmentsView",
    "AddDepartmentView",
    "UpdateDepartmentView",
    "ActivateDepartmentView",
    "DeactivateDepartmentView",
    "DeleteDepartmentView",
    # College Dean
    "CollegeDeansListView",
    "AddCollegeDeanView",
    "SelectCollegeDeanView",
    "CollegeDeanUpdateView",
    "CollegeDeanActivateView",
    "CollegeDeanDeactivateView",
    "RemoveFromCollegeDeanView",
    "CollegeDeanDeleteView",
    # Department Head
    "AllDepartmentHeadsListView",
    "CollegeDeanActivateView",
]
