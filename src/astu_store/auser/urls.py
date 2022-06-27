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
    # re_path(
    #     r"^add/college/representative/(?P<short_name>[A-Z]+)/$",
    #     views.AddCollegeRepresentativeView.as_view(),
    #     name="add_college_representative",
    # ),
]

# college_urlpatterns =

# department_urlpatterns = [


# ]


# department_representative_urlpatterns = [

# ]

list_urlpatterns = [
    re_path(r"^colleges/$", views.ListCollegesView.as_view(), name="list_colleges"),
]

urlpatterns = [
    re_path(r"^", include(list_urlpatterns)),
    re_path(r"^dashboard/$", views.DashboardView.as_view(), name="dashboard"),
    re_path(r"^auth/", include(django_auth_urlpatterns)),
    re_path(r"^import/(?P<pk>\d+)/$", views.ImportView.as_view(), name="import_data"),

    re_path(
        r"^college/",
        include(
            [
                re_path(r"^add/$", views.AddCollegeView.as_view(), name="add_college"),
                re_path(
                    r"^(?P<short_name>[A-Z]+)/",
                    include(
                        [
                            re_path(
                                r"^$",
                                views.CollegeDetailView.as_view(),
                                name="college_detail",
                            ),
                            re_path(
                                r"^update/$",
                                views.UpdateCollegeView.as_view(),
                                name="update_college",
                            ),
                            re_path(
                                r"^delete/$",
                                views.DeleteCollegeView.as_view(),
                                name="delete_college",
                            ),
                            re_path(
                                r"^activate/$",
                                views.ActivateCollegeView.as_view(),
                                name="activate_college",
                            ),
                            re_path(
                                r"^deactivate/$",
                                views.DeactivateCollegeView.as_view(),
                                name="deactivate_college",
                            ),
                            # College Representatives
                            re_path(
                                r"^representatives/",
                                include(
                                    [
                                        re_path(
                                            r"^$",
                                            views.CollegeRepresentativesListView.as_view(),
                                            name="college_representatives",
                                        ),
                                        re_path(
                                            r"^add/$",
                                            views.AddCollegeRepresentativeView.as_view(),
                                            name="add_college_representative",
                                        ),
                                        re_path(
                                            r"^(?P<pk>\d+)/",
                                            include(
                                                [
                                                    re_path(
                                                        r"^update/$",
                                                        views.CollegeRepresentativeUpdateView.as_view(),
                                                        name="update_college_representative",
                                                    ),
                                                    re_path(
                                                        r"^activate/$",
                                                        views.CollegeRepresentativeActivateView.as_view(),
                                                        name="activate_college_representative",
                                                    ),
                                                    re_path(
                                                        r"^deactivate/$",
                                                        views.CollegeRepresentativeDeactivateView.as_view(),
                                                        name="deactivate_college_representative",
                                                    ),
                                                    re_path(
                                                        r"^remove/$",
                                                        views.RemoveFromCollegeRepresentativeView.as_view(),
                                                        name="remove_college_representative",
                                                    ),
                                                    re_path(
                                                        r"^delete/$",
                                                        views.CollegeRepresentativeDeleteView.as_view(),
                                                        name="delete_college_representative",
                                                    ),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            # College Staff Members
                            re_path(
                                r"^staffs/",
                                include(
                                    [
                                        re_path(
                                            r"^$",
                                            views.CollegeStaffMembersListView.as_view(),
                                            name="college_staffs_list",
                                        ),
                                        re_path(
                                            r"^add/$",
                                            views.AddCollegeStaffMemberView.as_view(),
                                            name="add_college_staffs",
                                        ),
                                        re_path(
                                            r"(?P<pk>\d+)/",
                                            include(
                                                [
                                                    re_path(
                                                        r"^update/$",
                                                        views.CollegeStaffMemberUpdateView.as_view(),
                                                        name="update_college_staff",
                                                    ),
                                                    re_path(
                                                        r"^activate/$",
                                                        views.CollegeStaffMemberActivateView.as_view(),
                                                        name="activate_college_staff",
                                                    ),
                                                    re_path(
                                                        r"^deactivate/$",
                                                        views.CollegeStaffMemberDeactivateView.as_view(),
                                                        name="deactivate_college_staff",
                                                    ),
                                                    re_path(
                                                        r"^delete/$",
                                                        views.CollegeStaffMemberDeleteView.as_view(),
                                                        name="delete_college_staff",
                                                    ),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            # Collge Store Officer
                            re_path(
                                r"^store/officer/",
                                include(
                                    [
                                        re_path(
                                            r"^$",
                                            views.CollegeStoreOfficersListView.as_view(),
                                            name="college_store_officers_list",
                                        )
                                    ]
                                ),
                            ),
                            # Collge Lab assistant
                            re_path(
                                r"^lab/assistant/",
                                include(
                                    [
                                        re_path(
                                            r"^$",
                                            views.CollegeLabAssistantsOfficersListView.as_view(),
                                            name="college_lab_assistants_list",
                                        )
                                    ]
                                ),
                            ),
                            # Departments
                            re_path(
                                r"^departments/",
                                include(
                                    [
                                        re_path(
                                            r"^$",
                                            views.ListDepartmentsOfCollegeView.as_view(),
                                            name="list_departments_for_college",
                                        ),
                                        re_path(
                                            r"^add/$",
                                            views.AddDepartmentView.as_view(),
                                            name="add_department",
                                        ),
                                        re_path(
                                            r"^(?P<dept_short_name>[A-Z]+)/",
                                            include(
                                                [
                                                    re_path(
                                                        r"^$",
                                                        views.DepartmentDetailView.as_view(),
                                                        name="department_detail",
                                                    ),
                                                    re_path(
                                                        r"^update/$",
                                                        views.UpdateDepartmentView.as_view(),
                                                        name="update_department",
                                                    ),
                                                    re_path(
                                                        r"^activate/$",
                                                        views.ActivateDepartmentView.as_view(),
                                                        name="activate_department",
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
                                                    # Department Representatives
                                                    re_path(
                                                        r"^representatives/",
                                                        include(
                                                            [
                                                                re_path(
                                                                    r"^$",
                                                                    views.DepartmentRepresentativesListView.as_view(),
                                                                    name="department_representatives",
                                                                ),
                                                                re_path(
                                                                    r"^add/$",
                                                                    views.AddDepartmentRepresentativeView.as_view(),
                                                                    name="add_department_representative",
                                                                ),
                                                                re_path(
                                                                    r"^(?P<pk>\d+)/",
                                                                    include(
                                                                        [
                                                                            re_path(
                                                                                r"^update/$",
                                                                                views.DepartmentRepresentativeUpdateView.as_view(),
                                                                                name="update_department_representative",
                                                                            ),
                                                                            re_path(
                                                                                r"^activate/$",
                                                                                views.DepartmentRepresentativeActivateView.as_view(),
                                                                                name="activate_department_representative",
                                                                            ),
                                                                            re_path(
                                                                                r"^deactivate/$",
                                                                                views.DepartmentRepresentativeDeactivateView.as_view(),
                                                                                name="deactivate_department_representative",
                                                                            ),
                                                                            re_path(
                                                                                r"^remove/$",
                                                                                views.RemoveFromDepartmentRepresentativeView.as_view(),
                                                                                name="remove_department_representative",
                                                                            ),
                                                                            re_path(
                                                                                r"^delete/$",
                                                                                views.DepartmentRepresentativeDeleteView.as_view(),
                                                                                name="delete_department_representative",
                                                                            ),
                                                                        ]
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                    ),
                                                    # Department Staffs
                                                    re_path(
                                                        r"^staffs/",
                                                        include(
                                                            [
                                                                re_path(
                                                                    r"^$",
                                                                    views.DepartmentStaffMembersListView.as_view(),
                                                                    name="department_staffs_list",
                                                                ),
                                                                re_path(
                                                                    r"^add/$",
                                                                    views.AddDepartmentStaffMemberView.as_view(),
                                                                    name="add_department_staffs",
                                                                ),
                                                                re_path(
                                                                    r"^(?P<pk>\d+)/",
                                                                    include(
                                                                        [
                                                                            re_path(
                                                                                r"^update/$",
                                                                                views.DepartmentStaffMemberUpdateView.as_view(),
                                                                                name="update_department_staff",
                                                                            ),
                                                                            re_path(
                                                                                r"^activate/$",
                                                                                views.DepartmentStaffMemberActivateView.as_view(),
                                                                                name="activate_department_staff",
                                                                            ),
                                                                            re_path(
                                                                                r"^deactivate/$",
                                                                                views.DepartmentStaffMemberDeactivateView.as_view(),
                                                                                name="deactivate_department_staff",
                                                                            ),
                                                                            re_path(
                                                                                r"^delete/$",
                                                                                views.DepartmentStaffMemberDeleteView.as_view(),
                                                                                name="delete_department_staff",
                                                                            ),
                                                                        ]
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                    ),
                                                    # Department Store Officers
                                                    re_path(
                                                        r"^store/officer/",
                                                        include(
                                                            [
                                                                re_path(
                                                                    r"^$",
                                                                    views.DepartmentStoreOfficersListView.as_view(),
                                                                    name="department_store_officers_list",
                                                                )
                                                            ]
                                                        ),
                                                    ),
                                                    # Department Lab Assistants
                                                    re_path(
                                                        r"^lab/assistant/",
                                                        include(
                                                            [
                                                                re_path(
                                                                    r"^$",
                                                                    views.DepartmentLabAssistantsOfficersListView.as_view(),
                                                                    name="department_lab_assistants_list",
                                                                )
                                                            ]
                                                        ),
                                                    ),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    # re_path(
    #     r"^(?P<short_name>[A-Z]+)/department/representative/",
    #     include(department_representative_urlpatterns),
    # ),
]
