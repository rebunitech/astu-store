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
    re_path(r"^add/$", views.AddMaintenaceRequestView.as_view(), name="add_maintenace_request"),
    re_path(r"^list_maintenace_request/$", views.ListMaintenaceRequestView.as_view(), name="list_maintenacerequests"),
    # approve maintenance request 
    re_path(
        r"list_approve/$",
        views.ListApprovedMaintenanceRequestView.as_view(),
        name="lists_approved_request"
    ),
    # re_path(
    #     r"^detail/(?P<pk>\d+)/$",
    #     views.DetailFailureReprtView.as_view(),
    #     name="failure_detail",
    # ),

  
]

under_maintenance_urls = [
    re_path(r"^under_maintenace/$", views.ListUnderMaintenaceView.as_view(), name="list_undermaintenaces"),
    
]
urlpatterns = [
    re_path(r"^maintenace/", include(maintenace_urls)),
    re_path(r"under_maintenance/", include(under_maintenance_urls)),
    
]

