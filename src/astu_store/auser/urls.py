from django.contrib.auth.views import (LoginView, PasswordChangeView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.urls import include, path, re_path, reverse_lazy

from auser import views

app_name = "auser"

django_auth_urlpatterns = [
    re_path(
        r"^login/$",
        LoginView.as_view(
            redirect_authenticated_user=True,
            extra_context={"title": "Login"},
        ),
        name="login",
    ),
    re_path(
        r"^password_change/$",
        PasswordChangeView.as_view(
            success_url=reverse_lazy("pages:dashboard"),
            extra_context={"title": "Change Password"},
        ),
        name="password_change",
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
    re_path(r"", include("django.contrib.auth.urls")),
    re_path(
        r"^add/college/representative/$",
        views.AddCollegeRepresentativeView.as_view(),
        name="add_college_representative",
    ),
]

college_urlpatterns = [
    re_path(r"^add/$", views.AddCollegeView.as_view(), name="add_college"),
    re_path(
        r"^update/(?P<short_name>[A-Z]+)/$",
        views.UpdateCollegeView.as_view(),
        name="update_college",
    ),
    re_path(
        r"^delete/(?P<short_name>[A-Z]+)/$",
        views.DeleteCollegeView.as_view(),
        name="delete_college",
    ),
]

college_representative_urlpatterns = [
    re_path(
        r"^add/$",
        views.AddCollegeRepresentativeView.as_view(),
        name="add_college_representative",
    )
]

list_urlpatterns = [
    re_path(r"^colleges/$", views.ListCollegesView.as_view(), name="list_colleges"),
]

urlpatterns = [
    re_path(r"^", include(list_urlpatterns)),
    re_path(r"^dashboard/$", views.DashboardView.as_view(), name="dashboard"),
    re_path(r"^auth/", include(django_auth_urlpatterns)),
    re_path(r"^college/", include(college_urlpatterns)),
    re_path(r"^college/representative/", include(college_representative_urlpatterns)),
]
