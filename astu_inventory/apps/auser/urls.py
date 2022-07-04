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
        include([
            re_path(
                r"^$",
                views.ListRolesView.as_view(),
                name='roles_list'
            ),
            re_path(
                r"^update/(?P<pk>\d+)/$",
                views.UpdateRoleView.as_view(),
                name='update_role'
            )
        ])
    ),
]
