from .department import (
    ActivateDepartmentView,
    AddAllDepartmentHeadView,
    AddDepartmentHeadView,
    AddDepartmentView,
    AllDepartmentHeadActivateView,
    AllDepartmentHeadDeactivateView,
    AllDepartmentHeadDeleteView,
    AllDepartmentHeadsListView,
    AllDepartmentHeadUpdateView,
    AllRemoveFromDepartmentHeadView,
    AllSelectDepartmentHeadView,
    DeactivateDepartmentView,
    DeleteDepartmentView,
    DepartmentHeadActivateView,
    DepartmentHeadDeactivateView,
    DepartmentHeadDeleteView,
    DepartmentHeadsListView,
    DepartmentHeadUpdateView,
    ListDepartmentsView,
    RemoveFromDepartmentHeadView,
    SelectDepartmentHeadView,
    UpdateDepartmentView,
)
from .officer import (
    AddAllStoreOfficerView,
    AddStoreOfficerView,
    AllRemoveFromStoreOfficerView,
    AllStoreOfficerActivateView,
    AllStoreOfficerDeactivateView,
    AllStoreOfficerDeleteView,
    AllStoreOfficersListView,
    AllStoreOfficerUpdateView,
    RemoveFromStoreOfficerView,
    StoreOfficerActivateView,
    StoreOfficerDeactivateView,
    StoreOfficerDeleteView,
    StoreOfficersListView,
    StoreOfficerUpdateView,
)
from .role import ListRolesView, UpdateRoleView
from .staff_member import (
    ActivateStaffMemberView,
    AddStaffMemberView,
    AllAddStaffMemberView,
    AllDeactivateStaffMemberView,
    AllStaffMemberActivateView,
    AllStaffMemberDeleteView,
    AllStaffMemberListView,
    AllUpdateStaffMemberView,
    DeactivateStaffMemberView,
    DeleteStaffMemberView,
    StaffMemberListView,
    UpdateStaffMemberView,
)
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
    "DepartmentHeadsListView",
    "AddAllDepartmentHeadView",
    "AddDepartmentHeadView",
    "AllDepartmentHeadUpdateView",
    "DepartmentHeadUpdateView",
    "AllDepartmentHeadActivateView",
    "DepartmentHeadActivateView",
    "AllDepartmentHeadDeactivateView",
    "DepartmentHeadDeactivateView",
    "AllRemoveFromDepartmentHeadView",
    "RemoveFromDepartmentHeadView",
    "AllDepartmentHeadDeleteView",
    "DepartmentHeadDeleteView",
    "AllSelectDepartmentHeadView",
    "SelectDepartmentHeadView",
    # store officer
    "AddAllStoreOfficerView",
    "AddStoreOfficerView",
    "AllRemoveFromStoreOfficerView",
    "AllStoreOfficerActivateView",
    "AllStoreOfficerDeactivateView",
    "AllStoreOfficerDeleteView",
    "AllStoreOfficersListView",
    "AllStoreOfficerUpdateView",
    "RemoveFromStoreOfficerView",
    "StoreOfficerActivateView",
    "StoreOfficerDeactivateView",
    "StoreOfficerDeleteView",
    "StoreOfficersListView",
    "StoreOfficerUpdateView",
    # staff member
    "AllAddStaffMemberView",
    "AllStaffMemberListView",
    "AllUpdateStaffMemberView",
    "UpdateStaffMemberView",
    "StaffMemberListView",
    "AddStaffMemberView",
    "AllStaffMemberActivateView",
    "ActivateStaffMemberView",
    "DeactivateStaffMemberView",
    "AllDeactivateStaffMemberView",
    "AllStaffMemberDeleteView",
    "DeleteStaffMemberView",
]
