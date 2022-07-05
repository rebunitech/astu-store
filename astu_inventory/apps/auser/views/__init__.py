from .department import (
    ActivateDepartmentView,
    AddDepartmentView,
    DeactivateDepartmentView,
    DeleteDepartmentView,
    ListDepartmentsView,
    UpdateDepartmentView,
)
from .role import ListRolesView, UpdateRoleView
from .user import ProfileEditView

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
]
