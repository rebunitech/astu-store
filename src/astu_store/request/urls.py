from django.urls import path, re_path

from .import views
from .views import (  AddRequestView, BorrowDetailView, DeleteRequestView,
                     RequestDetailView, RequestListView,
                    )
app_name = "request"
urlpatterns = [
    path("request/", AddRequestView.as_view(), name="add_request"),
    # path("request_other/", MakeRequestOtherDepartment.as_view(), name="add_request_otherdept"),
    re_path(r"request_list/$",
            RequestListView.as_view(), 
            name="request_list"
            ),
    # path("add_item", AddItemView.as_view(), name="add_item"),
    # path("listItem", ListItemView.as_view(), name="item_list"),
    # path("edit/<int:pk>", ItemUpdateView.as_view(), name="item_edit"),
    path("delete/<int:pk>", DeleteRequestView.as_view(), name="request_delete"),
                              
    path("view/<int:pk>", RequestDetailView.as_view(), name="request_detail"),
    path("borrow_view/<int:pk>", BorrowDetailView.as_view(), name="borrow_detail"),  
    re_path(
        r"^approved_list/$",
        views.ListApprovedRequestView.as_view(),
        name="approved_list",
    ),
    re_path(
        r"^approve/(?P<pk>\d+)/$",
        views.ApproveUserRequest.as_view(),
        name="approve_request",
    ),
    re_path(
        r"^decline/(?P<pk>\d+)/$",
        views.DeclineUserRequest.as_view(),
        name="decline_request",
    ),

     re_path(
        r"^declined_list/$",
        views.ListDeclinedRequestView.as_view(),
        name="declined_list",
    ),
    re_path(
        r"^detailItem/(?P<pk>\d+)/$",
        views.DetailItemView.as_view(),
        name="detail_item"
    ),

     re_path(
        r"^complete_request/(?P<pk>\d+)/$",
        views.CompleteUserRequest.as_view(),
        name="complete_request",
    ),

     
    re_path(
        r"^borrowed_list/$",
        views.ListCompletedUserRequest.as_view(),
        name="borrowed_list",
    ),

    re_path(
        r"^return_request/(?P<pk>\d+)/$",
        views.ReturnRequestedItem.as_view(),
        name="return_request",
    ),

     re_path(
        r"^returned_list/$",
        views.ListReturnedUserRequest.as_view(),
        name="returned_list",
    ),  
    # 
    # re_path(
    #     r"ashu/$",
    #     views.table_search, 
    #     name="ashu"
    # ),

]
