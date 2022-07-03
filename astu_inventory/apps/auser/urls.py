"""ASTU Inventory auser URL Configuration

The `urlpatterns` list routes URLs to views.
"""

from django.contrib.auth.decorators import login_required
from django.urls import include, re_path
from django.views.generic import TemplateView

app_name = "auser"

urlpatterns = [
    re_path(
        r"^dashboard/$",
        login_required(TemplateView.as_view(template_name="dashboard.html", extra_context={"title": "Dashboard"})),
        name="dashboard",
    ),
]
