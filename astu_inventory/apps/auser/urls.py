"""ASTU Inventory auser URL Configuration

The `urlpatterns` list routes URLs to views.

    Date Created: 3 July, 2022
    Author: Wendirad Demelash(@wendirad)
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.urls import include, path, re_path, reverse_lazy
from django.views.generic import TemplateView

from astu_inventory.apps.auser import views

app_name = "auser"

urlpatterns = [
    re_path(
        r"^dashboard/$",
        login_required(TemplateView.as_view(template_name="dashboard.html", extra_context={"title": "Dashboard"})),
        name="dashboard",
    ),
    re_path(
        r"^auth/",
        include(
            [
                re_path(
                    r"^login/$",
                    LoginView.as_view(
                        redirect_authenticated_user=True,
                        extra_context={"title": "Login"},
                    ),
                    name="login",
                ),
                re_path(
                    r"^password_reset/$",
                    PasswordResetView.as_view(
                        success_url=reverse_lazy("auser:password_reset_done"),
                        extra_context={"title": "Reset Password"},
                    ),
                    name="password_reset",
                ),
                path(
                    "reset/<uidb64>/<token>/",
                    PasswordResetConfirmView.as_view(
                        success_url=reverse_lazy("auser:password_reset_complete"),
                        extra_context={"title": "Reset Password"},
                    ),
                    name="password_reset_confirm",
                ),
                re_path(
                    r"^password_change/$",
                    PasswordChangeView.as_view(
                        success_url=reverse_lazy("auser:password_change_done"),
                        extra_context={"title": "Change Password"},
                    ),
                    name="password_change",
                ),
                re_path(r"", include("django.contrib.auth.urls")),
                re_path(r"^profile/edit/$", views.ProfileEditView.as_view(), name="edit_profile"),
            ]
        ),
    ),
    re_path(
        r"^roles/",
        include(
            [
                re_path(r"^$", views.ListRolesView.as_view(), name="roles_list"),
                re_path(r"^update/(?P<pk>\d+)/$", views.UpdateRoleView.as_view(), name="update_role"),
            ]
        ),
    ),
    re_path(
        r"^departments/",
        include(
            [
                re_path(r"^$", views.ListDepartmentsView.as_view(), name="departments_list"),
                re_path(r"^add/$", views.AddDepartmentView.as_view(), name="add_department"),
                re_path(r"^heads/$", views.AllDepartmentHeadsListView.as_view(), name="all_department_heads_list"),
                re_path(
                    r"^college/deans/",
                    include(
                        [
                            re_path(r"^$", views.CollegeDeansListView.as_view(), name="college_deans_list"),
                            re_path(r"^add/$", views.AddCollegeDeanView.as_view(), name="add_college_dean"),
                            re_path(r"^select/$", views.SelectCollegeDeanView.as_view(), name="select_college_dean"),
                            re_path(
                                r"^(?P<pk>\d+)/",
                                include(
                                    [
                                        re_path(
                                            r"^update/$",
                                            views.CollegeDeanUpdateView.as_view(),
                                            name="update_college_dean",
                                        ),
                                        re_path(
                                            r"^activate/$",
                                            views.CollegeDeanActivateView.as_view(),
                                            name="activate_college_dean",
                                        ),
                                        re_path(
                                            r"^deactivate/$",
                                            views.CollegeDeanDeactivateView.as_view(),
                                            name="deactivate_college_dean",
                                        ),
                                        re_path(
                                            r"^remove/$",
                                            views.RemoveFromCollegeDeanView.as_view(),
                                            name="remove_college_dean",
                                        ),
                                        re_path(
                                            r"^delete/$",
                                            views.CollegeDeanDeleteView.as_view(),
                                            name="delete_college_dean",
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
                re_path(
                    r"^(?P<short_name>[a-zA-Z0-9\_\-]+)/",
                    include(
                        [
                            re_path(r"^update/$", views.UpdateDepartmentView.as_view(), name="update_department"),
                            re_path(
                                r"^activate/$", views.ActivateDepartmentView.as_view(), name="activate_department"
                            ),
                            re_path(
                                r"^deactivate/$",
                                views.DeactivateDepartmentView.as_view(),
                                name="deactivate_department",
                            ),
                            re_path(
                                r"^delete/$",
                                views.DeleteDepartmentView.as_view(),
                                name="delete_department",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
]
