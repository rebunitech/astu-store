"""astu_inventory URL Configuration

The `urlpatterns` list routes URLs to views.

    Date Created: 3 July, 2022
    Author: Wendirad Demelash(@wendirad)
"""
import importlib

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path, reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    re_path(r"", include("astu_inventory.apps.auser.urls")),
    re_path(r"", include("astu_inventory.apps.core.urls")),
    re_path(r"^inventory/", include("astu_inventory.apps.inventory.urls")),
    re_path(r"^help/", include("astu_inventory.apps.help.urls")),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^chaining/", include("smart_selects.urls")),
    re_path(r"^summernote/", include("django_summernote.urls")),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("core:dashboard"))),
]

if settings.DEBUG:
    debug_toolbar = importlib.import_module("debug_toolbar")

    urlpatterns.append(re_path(r"^__debug__/", include(debug_toolbar.urls)))
