"""gradient_infosys auser URL Configuration
	
    Created by: Wendirad Demelash
    Last modified by: Wendirad Demelash
"""

from django.contrib.auth.views import (LoginView, PasswordChangeView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.urls import include, path, re_path, reverse_lazy

from auser import views
from auser.forms import LoginForm

app_name = "auser"

django_auth_urlpatterns = [
    re_path(
        r"^login/$",
        LoginView.as_view(
            form_class=LoginForm,
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
    re_path(
        r"^password_reset/done/$",
        views.PasswordResetDoneView.as_view(),
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
    re_path(r"^profile/edit/$", views.ProfileEditView.as_view(), name="profile_edit"),
    re_path(
        r"^user/permissions/(?P<pk>\d+)/$",
        views.ChangePermissionView.as_view(),
        name="change_permission",
    ),
    re_path(
        r"^user/logs/(?P<pk>\d+)/$",
        views.UserActionsListView.as_view(),
        name="user_logs", 
    ),
]

staff_urlpatterns = [
    re_path(
        r"^$",
        views.ListActiveStaffUsersView.as_view(),
        name="active_staff_list",
    ),
    re_path(r"^add/$", views.AddStaffUserView.as_view(), name="staff_add"),
    re_path(
        r"^deactivated/$",
        views.ListDeactivatedStaffUsersView.as_view(),
        name="deactivated_staff_list",
    ),
    re_path(
        r"^deactivate/(?P<pk>\d+)/$",
        views.DeactivateStaffUserView.as_view(),
        name="deactivate_staff",
    ),
    re_path(
        r"^update/(?P<pk>\d+)/$",
        views.UpdateStaffUserView.as_view(),
        name="staff_update",
    ),
    re_path(
        r"^activate/(?P<pk>\d+)/$",
        views.ActivateStaffUserView.as_view(),
        name="activate_staff",
    ),
    re_path(
        r"^delete/(?P<pk>\d+)/$",
        views.DeleteStaffUserView.as_view(),
        name="delete_staff",
    ),
    re_path(
        r"^detail/(?P<pk>\d+)/$",
        views.StaffUserDetailView.as_view(),
        name="staff_detail",
    ),
]

# content_creator_urlpatterns = [
#     re_path(
#         r"^$",
#         views.ListActiveContentCreatorsView.as_view(),
#         name="active_content_creator_list",
#     ),
#     re_path(
#         r"^add/$", views.AddContentCreatorView.as_view(), name="content_creator_add"
#     ),
#     re_path(
#         r"^deactivated/$",
#         views.ListDeactivatedContentCreatorsView.as_view(),
#         name="deactivated_content_creator_list",
#     ),
#     re_path(
#         r"^deactivate/(?P<pk>\d+)/$",
#         views.DeactivateContentCreatorView.as_view(),
#         name="deactivate_content_creator",
#     ),
#     re_path(
#         r"^update/(?P<pk>\d+)/$",
#         views.UpdateContentCreatorView.as_view(),
#         name="content_creator_update",
#     ),
#     re_path(
#         r"^activate/(?P<pk>\d+)/$",
#         views.ActivateContentCreatorView.as_view(),
#         name="activate_content_creator",
#     ),
#     re_path(
#         r"^delete/(?P<pk>\d+)/$",
#         views.DeleteContentCreator.as_view(),
#         name="delete_content_creator",
#     ),
#     re_path(
#         r"^detail/(?P<pk>\d+)/$",
#         views.ContentCreatorDetailView.as_view(),   
#         name="content_creator_detail",
#     ),
# ]

student_urlpatterns = [
    re_path(r"^$", views.ListActiveStudentsView.as_view(), name="active_student_list"),
    re_path(
        r"^deactivated/$",
        views.ListDeactivatedStudentsView.as_view(),
        name="deactivated_student_list",
    ),
    re_path(
        r"^activate/(?P<pk>\d+)/$",
        views.ActivateStudentView.as_view(),
        name="activate_student",
    ),
    re_path(
        r"^deativate/(?P<pk>\d+)/$",
        views.DeactivateStudentView.as_view(),
        name="deactivate_student",
    ),
    re_path(
        r"^delete/(?P<pk>\d+)/$",
        views.DeleteStudentView.as_view(),
        name="delete_student",
    ),
    re_path(
        r"^detail/(?P<pk>\d+)/$",
        views.StudentDetailView.as_view(),
        name="student_detail",
    ),
]

# instructor_urlpatterns = [
#     re_path(
#         r"^$", views.InstructorListAdminView.as_view(), name="instructor_list_admin"
#     ),
#     re_path(r"^add/$", views.AddInstructorView.as_view(), name="instructor_add"),
#     re_path(
#         r"^detail/(?P<pk>\d+)/$",
#         views.InstructorDetailAdminView.as_view(),
#         name="instructor_detail_admin",
#     ),
#     re_path(
#         r"^update/(?P<pk>\d+)/$",
#         views.UpdateInstructorView.as_view(),
#         name="instructor_update",
#     ),
#     re_path(
#         r"^delete/(?P<pk>\d+)/$",
#         views.DeleteInstructorView.as_view(),
#         name="instructor_delete",
#     ),
#     re_path(
#         r"^social_link/add/(?P<instructor_pk>\d+)/$",
#         views.AddInstructorSocialMediaLinkView.as_view(),
#         name="instructor_social_link_add",
#     ),
#     re_path(
#         r"^social_link/update/(?P<pk>\d+)/$",
#         views.UpdateInstructorSocialMediaLinkView.as_view(),
#         name="instructor_social_link_update",
#     ),
#     re_path(
#         r"^social_link/delete/(?P<pk>\d+)/$",
#         views.DeleteInstructorSocialMediaLinkView.as_view(),
#         name="instructor_social_link_delete",
#     ),
#     re_path(
#         r"^education_background/add/(?P<instructor_pk>\d+)/$",
#         views.AddEducationBackgroundView.as_view(),
#         name="instructor_education_background_add",
#     ),
#     re_path(
#         r"^education_background/update/(?P<pk>\d+)/$",
#         views.UpdateEducationBackgroundView.as_view(),
#         name="instructor_education_background_update",
#     ),
#     re_path(
#         r"^education_background/delete/(?P<pk>\d+)/$",
#         views.DeleteEducationBackgroundView.as_view(),
#         name="instructor_education_background_delete",
#     ),
#     re_path(
#         r"^experience/add/(?P<instructor_pk>\d+)/$",
#         views.AddExperienceView.as_view(),
#         name="instructor_experience_add",
#     ),
#     re_path(
#         r"^experience/update/(?P<pk>\d+)/$",
#         views.UpdateExperienceView.as_view(),
#         name="instructor_experience_update",
#     ),
#     re_path(
#         r"^experience/delete/(?P<pk>\d+)/$",
#         views.DeleteExperienceView.as_view(),
#         name="instructor_experience_delete",
#     ),
# ]


# social_media_urlpatterns = [
#     re_path(
#         r"^add/$",
#         views.AddSocialMediaView.as_view(),
#         name="social_media_add", 
#     ),
#     re_path(
#         r"^update/(?P<pk>\d+)/$",
#         views.UpdateSocialMediaView.as_view(),
#         name="social_media_update",
#     ),
#     re_path(
#         r"^delete/(?P<pk>\d+)/$",
#         views.DeleteSocialMediaView.as_view(),
#         name="social_media_delete",
#     ),
# ]

urlpatterns = [
    re_path(r"", include(django_auth_urlpatterns)),
    re_path(r"", include(user_urlpatterns)),
    re_path(r"^register/$", views.SignUpView.as_view(), name="register"),
    re_path(r"^staff/", include(staff_urlpatterns)),
    re_path(r"^student/", include(student_urlpatterns)),
    # re_path(r"^content_creator/", include(content_creator_urlpatterns)),
    # re_path(r"^instructor/", include(instructor_urlpatterns)),
    # re_path(r"^social_media/", include(social_media_urlpatterns)),
    re_path(r"^import/(?P<pk>\d+)/$", views.ImportView.as_view(), name="import_data"),
    re_path(r"", include("django.contrib.auth.urls")),
]
