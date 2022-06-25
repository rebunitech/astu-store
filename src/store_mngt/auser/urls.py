"""gradient_infosys auser URL Configuration
	
    Created by: Ashenafi Zenebe
"""
from unicodedata import name
from django.urls import re_path, include, reverse_lazy, path
from django.contrib.auth.views import (LoginView, PasswordChangeView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from auser import view  
from auser.forms import LoginForm

app_name = "auser"

django_auth_urlpattern = [
    re_path(r"^dashboard/$", view.DashboardView.as_view(), name="dashboard"),

    re_path(
        r"^login/$",
        LoginView.as_view(
            form_class = LoginForm,
            redirect_authenticated_user = True,
            extra_context = {"title": "Login"}
        ),
        name="login",
    ),
    re_path(
        r"^password_change/$",
        PasswordChangeView.as_view(
            success_url=reverse_lazy("auser:dashboard"),
            extra_context = {"title": "Change Password"},
        ),
        name = "password_change",
    ),
    re_path(
        r"^password_reset/$",
        PasswordResetView.as_view(
            success_url=reverse_lazy("auser:password_reset_done"),
            extra_context={"title": "Reset Password"},
        ),
        name="password_reset",
    ),
    re_path(
        r"^password_reset/done/$",
        view.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("auser:password_reset_complete"),
            extra_context={"title": "Reset Password"},
        ),
        name="password_reset_confirm",
    ),
]


user_urlpatterns = [
    re_path(
        r"^profile/edit/$",
         view.ProfileEditView.as_view(),
          name="profile_edit"),
    re_path(
        r"^user/permissions/(?P<pk>\d+)/$",
        view.ChangePermissionView.as_view(),
        name="change_permission",
    ),
    re_path(
        r"^user/logs/(?P<pk>\d+)/$",
        view.UserActionsListView.as_view(),
        name="user_logs", 
    ),
]

schoolHead_urlpatterns = [
    re_path(
        r"^$",
        view.ListActiveSchoolHeadsView.as_view(),
        name="active_school_head_list",
    ),
    re_path(
        r"^add/$",
        view.AddSchoolHeadView.as_view(),
        name="add_school_head"
    ),
    re_path(
        r"^deactivated/$",
        view.ListDeactivatedSchoolHeadsView.as_view(),
        name="deactivated_school_head_list",
    ),
    re_path(
        r"^deactivate/(?P<pk>\d+)/$",
        view.DeactivateSchoolHeadView.as_view(),
        name="deactivate_school_head",
    ),
    re_path(
        r"^update/(?P<pk>\d+)/$",
        view.UpdateSchoolHeadView.as_view(),
        name="school_head_update",
    ),
    re_path(
        r"^activate/(?P<pk>\d+)/$",
        view.ActivateSchoolHeadView.as_view(),
        name="activate_school_head",
    ),
    re_path(
        r"^delete/(?P<pk>\d+)/$",
        view.DeleteSchoolHeadView.as_view(),
        name="delete_school_head",
    ),
    re_path(
        r"^detail/(?P<pk>\d+)/$",
        view.SchoolHeadDetailView.as_view(),
        name="school_head_detail",
    ),
]

department_head_urlpatterns =[
    re_path(
        r"^$",
        view.ListActiveDepartmentHeadsView.as_view(),
        name="active_department_head_list",
    ),
    re_path(
        r"^add/$", 
        view.AddDepartmenHead.as_view(),
        name="department_head_add"
    ),
    re_path(
        r"^deactivated/$",
        view.ListDeactivatedDepartmentHeadsView.as_view(),
        name="deactivated_department_head_list",
    ),
    re_path(
        r"^deactivate/(?P<pk>\d+)/$",
        view.DeactivateDepartmentHeadView.as_view(),
        name="deactivate_department_head",
    ),
    re_path(
        r"^update/(?P<pk>\d+)/$",
        view.UpdateDepartmentHead.as_view(),
        name="department_head_update",
    ),
    re_path(
        r"^activate/(?P<pk>\d+)/$",
        view.ActivateDepartmentHeadView.as_view(),
        name="activate_department_head",
    ),
    re_path(
        r"^delete/(?P<pk>\d+)/$",
        view.DeleteDepartmentHead.as_view(),
        name="delete_department_head",
    ),
    re_path(
        r"^detail/(?P<pk>\d+)/$",
        view.DepartmentHeadDetailView.as_view(),   
        name="department_head_detail",
    ),
]

store_keeper_urlpatterns = [
    re_path(
        r"^$",
        view.ListActiveStoreKeepersView.as_view(),
        name="active_store_keeper_list",
    ),
    re_path(
        r"^add/$", 
        view.AddStoreKeeper.as_view(),
        name="store_keeper_add"
    ),
    re_path(
        r"^deactivated/$",
        view.ListDeactivatedStoreKeepersView.as_view(),
        name="deactivated_store_keeper_list",
    ),
    re_path(
        r"^deactivate/(?P<pk>\d+)/$",
        view.DeactivateStoreKeeperView.as_view(),
        name="deactivate_store_keeper",
    ),
    re_path(
        r"^update/(?P<pk>\d+)/$",
        view.UpdateStoreKeeper.as_view(),
        name="store_keeper_update",
    ),
    re_path(
        r"^activate/(?P<pk>\d+)/$",
        view.ActivateStoreKeeperView.as_view(),
        name="activate_store_keeper",
    ),
    re_path(
        r"^delete/(?P<pk>\d+)/$",
        view.DeleteStoreKeeprView.as_view(),
        name="delete_store_keeper",
    ),
    re_path(
        r"^detail/(?P<pk>\d+)/$",
        view.StoreKeeperDetailView.as_view(),   
        name="store_keeper_detail",
    ),
]


staffmember_urlpatterns = [
    re_path(r"^$", 
            view.ListActiveStaffMembersView.as_view(),
            name="active_staffmember_list"),
    re_path(
        r"^add/$", 
        view.AddStaffMember.as_view(),
        name="staffmember_add"
    ),
    re_path(
        r"^update/(?P<pk>\d+)/$",
        view.UpdateStaffMember.as_view(),
        name="staffmember_update",
    ),
    re_path(
        r"^deactivated/$",
        view.ListDeactivatedStaffMembersView.as_view(),
        name="deactivated_staffmember_list",
    ),
    re_path(
        r"^activate/(?P<pk>\d+)/$",
        view.ActivateStaffMemberView.as_view(),
        name="activate_staffmember",
    ),
    re_path(
        r"^deativate/(?P<pk>\d+)/$",
        view.DeactivateStaffMemberView.as_view(),
        name="deactivate_staffmember",
    ),
    re_path(
        r"^delete/(?P<pk>\d+)/$",
        view.DeleteStaffMemberView.as_view(),
        name="delete_staffmember",
    ),
    re_path(
        r"^detail/(?P<pk>\d+)/$",
        view.StaffMemberDetailView.as_view(),
        name="staffmember_detail",
    ),
]


department_urlpatterns = [
    re_path(r"^$",  
                view.ListActiveDepartmentView.as_view(), 
                name="active_department_list"
                ),
    re_path(
        r"deactivated/$",
        view.ListDeactiveDepartmentView.as_view(),
        name="list_deactivate_department",
    ),
    re_path(
        r"^add/$",
        view.AddDepartmentView.as_view(),
        name="add_department",
    ),
    re_path(
        r"^delete/(?P<pk>\d+)/$",
        view.DeleteDepartment.as_view(),
        name="delete_department",
    ),
    re_path(
        r"^update/(?P<pk>\d+)/$",
        view.UpdateDepartmentView.as_view(),
        name="update_department",
    ),
    re_path(
        r"^deactivate/(?P<pk>\d+)/$",
        view.DeactivateDepartmentView.as_view(),
        name="deactivate_department",
    ),
    re_path(
        r"^activate/(?P<pk>\d+)/$",
        view.ActivateDepartmentView.as_view(),
        name="activate_department",
    ),
    re_path(
        r"^detail/(?P<pk>\d+)/$",
        view.DepartmentDetailView.as_view(),
        name="department_detail",
    ),
]

school_urlpatterns = [
    re_path( r"^$",
            view.ListActiveSchoolView.as_view(),
            name="active_school_list",
    ),
    re_path(
        r"^deactivated/$",
        view.ListDeactivatedSchoolView.as_view(),
        name="list_deactivated_school",
    ),
    re_path(
        r"^add/$",
        view.AddSchoolView.as_view(),
        name="add_school"
    ),
    re_path(
        r"^update/(?P<pk>\d+)/$",
        view.UpdateSchoolView.as_view(),
        name="update_school",
    ),
    re_path(
        r"^deactivate/(?P<pk>\d+)/$",
        view.DeactivateSchoolView.as_view(),
        name="deactivate_school",
    ),
    re_path(
        r"^activate/(?P<pk>\d+)/$",
        view.ActivateSchoolView.as_view(),
        name="activate_school",
    ),
    re_path(
        r"^delete/(?P<pk>\d+)/$",
        view.DeleteSchool.as_view(),
        name="delete_school",),
    re_path(
        r"^detail/(?P<pk>\d+)/$",
        view.SchoolDetailView.as_view(),
        name="school_detail",),
    
]

urlpatterns = [
    re_path(r"", include(django_auth_urlpattern)),
    re_path(r"", include(user_urlpatterns)),
    re_path(r"^register/$", view.SignUpView.as_view(), name="register"),

    re_path(r"^schoolhead/", include(schoolHead_urlpatterns)),
    re_path(r"^departmenthead/", include(department_head_urlpatterns)),
    re_path(r"^storekeeper/", include(store_keeper_urlpatterns)),
    re_path(r"^staffmember/", include(staffmember_urlpatterns)),
    re_path(r"^import/(?P<pk>\d+)/$", view.ImportView.as_view(), name="import_data"),
    re_path(r"", include("django.contrib.auth.urls")),
    re_path(r"^department/", include(department_urlpatterns)),
    re_path(r"^school/", include(school_urlpatterns)),

]

