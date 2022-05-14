
from django.urls import re_path, include
from auser.view.departmentHead import AddDepartmenHead

urlpatterns = [
    re_path(r"register/$", AddDepartmenHead.as_view(), name="register"),
]