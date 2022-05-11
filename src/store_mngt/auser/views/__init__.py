from os import rename


# TODO: rename content_creator to department_head

from .content_creator import (ActivateDepartmentheadView,
                              AddDepartmentHeadView, DepartmentHeadDetailView,
                              DeactivateDepartmentHeadView,
                              DeleteDepartmentHead,
                              ListActiveDepartmentsView,
                              ListDeactivatedDepartmentHeadsView,
                              UpdateDepartmentHeadView)


from .staff import (ActivateStaffUserView, AddStaffUserView,
                    DeactivateStaffUserView, DeleteStaffUserView,
                    ListActiveStaffUsersView, ListDeactivatedStaffUsersView,
                    StaffUserDetailView, UpdateStaffUserView)
from .student import (ActivateStudentView, DeactivateStudentView,
                      DeleteStudentView, ListActiveStudentsView,    
                      ListDeactivatedStudentsView, SignUpView,
                      StudentDetailView)
from .user import (ChangePermissionView, PasswordResetDoneView,
                   ProfileEditView, UserActionsListView)
from .views import DashboardView, ImportView

__all__ = [
    "ActivateStaffUserView",
    "AddStaffUserView",
    "ChangePermissionView",
    "DeleteStaffUserView",
    "DeactivateStaffUserView",
    "ListActiveStaffUsersView",
    "ListDeactivatedStaffUsersView",
    "ProfileEditView",
    "UpdateStaffUserView",
    "DashboardView",
    "ListActiveDepartmentsView",
    "ListDeactivatedDepartmentHeadsView",
    "AddDepartmentHeadView",
    "DeactivateDepartmentHeadView",
    "UpdateDepartmentHeadView",
    "ActivateDepartmentheadView",
    "DeleteDepartmentHead",
    "DepartmentHeadDetailView",
    "DeleteStudentView",
    "UserActionsListView",
    "ListActiveStudentsView",
    "ListDeactivatedStudentsView",
    "ActivateStudentView",
    "DeactivateStudentView",
    "SignUpView",
    "PasswordResetDoneView",
    "ImportView",
    "StaffUserDetailView",
    "StudentDetailView",

]
