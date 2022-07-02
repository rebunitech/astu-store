"""astu_inventory URL Configuration

The `urlpatterns` list routes URLs to views.
"""
import importlib

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

if settings.DEBUG:
    debug_toolbar = importlib.import_module("debug_toolbar")

    urlpatterns.append(re_path(r"^__debug__/", include(debug_toolbar.urls)))
