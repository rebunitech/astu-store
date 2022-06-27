from django.urls import include, re_path

from maintenance import views

app_name = "maintenance"

maintenance_urls = [
    
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
    re_path(
        r"^detail/(?P<pk>\d+)/$",
        views.DetailFailureReprtView.as_view(),
        name="failure_detail",
    ),
    # list failurety url
    re_path(
        r"^add/$",
        views.AddMaintenanceRequestView.as_view(),
        name="add_maintenace_request"),
    re_path(
        r"^list_maintenace_request/$", 
        views.ListMaintenanceRequestView.as_view(), 
        name="list_maintenancerequests"
        ),
     
    re_path(
        r"update/(?P<pk>\d+)/$",
        views.UpdateMaintenanceRequestView.as_view(),
        name="update_maintenance_request",
    ),
    # cancel maintenance request 
    re_path(
        r"cancel/(?P<pk>\d+)/$",
        views.CancelMaintenanceRequestView.as_view(),
        name="cancel_maintenance_request"
    ),
    # url for canceled request lists
    re_path(
        r"canceled_request/$",
        views.CanceledListMaintenanceRequestView.as_view(),
        name="canceled_list",
    ),
    # approve maintenance request 
    re_path(
        r"approve/(?P<pk>\d+)/$",
        views.ApproveMaintenanceRequestView.as_view(),
        name="approve_maintenance_request",
    ),
    re_path(
        r"list_approve/$",
        views.ListApprovedMaintenanceRequestView.as_view(),
        name="lists_approved_request"
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
        r"damaged_requests/(?P<pk>\d+)/$",
        views.AddDamagedMaintenanceRequestView.as_view(),  
        name="damaged_requests",
    ),
       
    #  damaged requests lists url
     re_path(
        r"damaged_requests/$",
        views.ListDamagedMaintenanceRequestView.as_view(),
        name="damaged_requests_lists",
    ),     
    # reppaired maintenace request view 
    re_path (
        r"repaired_request/(?P<pk>\d+)/$",
        views.RepairedMaintenanceRequestView.as_view(),
        name = "repaired_request_list"
        
    ),
    re_path (
        r"repaired_request/(?P<pk>\d+)/$",
        views.ListDamagedMaintenanceRequestView.as_view(),
        name = "list_repaired_request_list"
            ),

]


urlpatterns = [
    re_path(r"^maintenance/", include(maintenance_urls)),
    
]

