from django.urls import include, re_path

from maintenace import views

app_name = "maintenace"

maintenace_urls = [
    
    re_path(
        r"^add_failurity/$", 
        views.AddFailurityReportView.as_view(), 
        name="add_failurirtyreports"
        ),
    re_path(
        r"list_failurity/$",
        views.ListFailurityReportView.as_view(),
        name="list_failurity_report"
    ),
    # list failurety url
    re_path(
        r"^add/$",
        views.AddMaintenaceRequestView.as_view(),
        name="add_maintenace_request"),
    re_path(
        r"^list_maintenace_request/$", 
        views.ListMaintenaceRequestView.as_view(), 
        name="list_maintenacerequests"
        ),
    
    # approve maintenance request 
    re_path(
        r"approve/(?P<pk>\d+)/$",
        views.ApproveMaintenanceRequestView.as_view(),
        name="approve_maintenance_request",
    ),
    
    # decline maintenace request
    re_path(
        r"decline/(?P<pk>\d+)/$",
        views.DeclinedMaintenanceRequestView.as_view(),
        name="decline_maintenance_request",
    ),
    
    re_path(
        r"decline/$",
        views.ListDeclinedMaintenanceRequestView.as_view(),
        name="lists_declined_request"
    ),
    
    
    
     
    
    re_path(
        r"list_approve/$",
        views.ListApprovedMaintenanceRequestView.as_view(),
        name="lists_approved_request"
    ),
    re_path(
        r"update/(?P<pk>\d+)/$",
        views.UpdateMaintenanceRequestView.as_view(),
        name="update_maintenance_request",
    ),
    re_path(
        r"^detail/(?P<pk>\d+)/$",
        views.DetailFailureReprtView.as_view(),
        name="failure_detail",
    ),
        # cancel maintenance request 

    re_path(
        r"cancel/(?P<pk>\d+)/$",
        views.CancelMaintenaceRequestView.as_view(),
        name="cancel_maintenance_request"
    ),
    re_path(
        r"canceled_request/$",
        views.CanceledListMaintenanceRequestView.as_view(),
        name="canceled_list",
    ),
  
]


urlpatterns = [
    re_path(r"^maintenace/", include(maintenace_urls)),
    
]

