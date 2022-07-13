from django.urls import re_path

from astu_inventory.apps.help import views

app_name = "help"

urlpatterns = [
    re_path(r"^$", views.ListHelpsView.as_view(), name="helps_list"),
    re_path(r"(?P<pk>\d+)/update/$", views.UpdateHelpView.as_view(), name="update_help"),
]
