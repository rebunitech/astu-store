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
    # url for canceled request lists
    re_path(
        r"canceled_request/$",
        views.CanceledListMaintenanceRequestView.as_view(),
        name="canceled_list",
    ),
    
     re_path(
        r"Add_damage_reports/$",
        views.AddDamageReportView.as_view(),
        name= "add_damagereports",
    ),
  
       
  # list of damage report url
    re_path(
        r"list_damage_reports/$",
        views.ListDamageReportView.as_view(),
        name="list_damagereports",
    ),
      #  damaged requests url

     re_path(
        r"damaged_requests/(?P<pk>\d+)/(?P<item_pk>\d+)/$",
        views.AddDamagedMaintenaceRequestView.as_view(),  
        name="damaged_requests",
    ),
       
 #  damaged requests lists url

     re_path(
        r"damaged_requests/$",
        views.ListDamagedMaintenaceRequestView.as_view(),
        name="damaged_requests_lists",
    ),
     
# reppaired maintenace request view 

re_path (
    r"repaired_request/(?P<pk>\d+)/$",
    views.RepairedMaintenaceRequestView.as_view(),
    name = "repaired_request_list"
    
),

re_path (
    r"repaired_request/(?P<pk>\d+)/$",
    views.ListDamagedMaintenaceRequestView.as_view(),
    name = "list_repaired_request_list"
    
),

]


urlpatterns = [
    re_path(r"^maintenace/", include(maintenace_urls)),
    
]

