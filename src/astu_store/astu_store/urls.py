"""astu_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path, reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"", include("auser.urls")),
    re_path(r"", include("store.urls")),
    re_path(r"^chaining/", include("smart_selects.urls")),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("auser:dashboard"))),
]