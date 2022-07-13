from django.urls import re_path

from astu_inventory.apps.help import views

urlpatterns = [
    re_path(
        r"^add/$", views.AddHelpView.as_view(), name="add_help"
    )
]
