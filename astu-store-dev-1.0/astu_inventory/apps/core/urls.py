from django.urls import include, re_path

from astu_inventory.apps.core import views

app_name = "core"

urlpatterns = [
    re_path(
        r"^dashboard/$",
        views.ListAvailableProductsView.as_view(),
        name="dashboard",
    ),
    re_path(
        r"^products/",
        include(
            [
                re_path(
                    r"^borrow/request/",
                    include(
                        [
                            re_path(
                                r"^active/$",
                                views.ListActiveBorrowRequestView.as_view(),
                                name="active_borrow_requests_list",
                            ),
                            re_path(
                                r"^approved/$",
                                views.ListApprovedBorrowRequestView.as_view(),
                                name="approved_borrow_requests_list",
                            ),
                            re_path(
                                r"^completed/$",
                                views.ListCompletedBorrowRequestView.as_view(),
                                name="completed_borrow_requests_list",
                            ),
                            re_path(
                                r"^history/$",
                                views.ListBorrowRequestHistoryView.as_view(),
                                name="borrow_request_history_list",
                            ),
                            re_path(
                                r"^active/(?P<pk>\d+)/$",
                                views.ActiveBorrowRequestDetailView.as_view(),
                                name="active_borrow_requests_detail",
                            ),
                            re_path(
                                r"^approved/(?P<pk>\d+)/$",
                                views.ApprovedBorrowRequestDetailView.as_view(),
                                name="approved_borrow_requests_detail",
                            ),
                            re_path(
                                r"^completed/(?P<pk>\d+)/$",
                                views.CompletedBorrowRequestDetailView.as_view(),
                                name="completed_borrow_requests_detail",
                            ),
                            re_path(
                                r"^(?P<pk>\d+)/",
                                include(
                                    [
                                        re_path(
                                            r"^approve/$",
                                            views.ApproveBorrowRequestView.as_view(),
                                            name="approve_borrow_request",
                                        ),
                                        re_path(
                                            r"^decline/$",
                                            views.DeclineBorrowRequestView.as_view(),
                                            name="decline_borrow_request",
                                        ),
                                        re_path(
                                            r"^complete/$",
                                            views.CompleteBorrowRequestView.as_view(),
                                            name="complete_borrow_request",
                                        ),
                                        re_path(
                                            r"^revoke/$",
                                            views.RevokeBorrowRequestView.as_view(),
                                            name="revoke_borrow_request",
                                        ),
                                        re_path(
                                            r"^return/$",
                                            views.ReturnedBorrowRequestView.as_view(),
                                            name="return_borrow_request",
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
                re_path(
                    r"^(?P<slug>[-a-zA-Z0-9_]+)/borrow/request/",
                    include(
                        [
                            re_path(
                                r"^$",
                                views.InitiateBorrowRequestView.as_view(),
                                name="initiate_borrow_request",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
]
