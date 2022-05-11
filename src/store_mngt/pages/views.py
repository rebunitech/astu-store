from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.flatpages.models import FlatPage
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, TemplateView

# from .forms import (AddServiceForm, FlatPageForm, UpdateAdsForm,
#                     UpdateServiceForm)
# from .models import Ad, Service

from .forms import FlatPageForm
from django.utils.translation import gettext_lazy as _

class DashboardView(LoginRequiredMixin, TemplateView):   
    """Generic view for users dashboard."""

    template_name = "pages/dashboard.html"
    extra_context = {"title": _("Dashboard")}

# class ListServiceView(PermissionRequiredMixin, ListView):
#     model = Service
#     template_name = "services/list_service.html"
#     context_object_name = "services"
#     permission_required = "pages.view_service"
#     extra_context = {"title": "Services"}


# class AddServiceView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Service
#     form_class = AddServiceForm
#     template_name = "services/add_service.html"
#     permission_required = ("pages.add_service",)
#     success_url = reverse_lazy("pages:list-service")
#     extra_context = {"title": "Add Service"}
#     success_message = '"%(title)s" added successfully!'


# class UpdateServiceView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = Service
#     form_class = UpdateServiceForm
#     template_name = "services/update_service.html"
#     permission_required = ("pages.change_service",)
#     success_url = reverse_lazy("pages:list-service")
#     extra_context = {"title": "Update Service"}
#     success_message = "%(title)s update successfully!"


# class DeleteServiceView(PermissionRequiredMixin, DeleteView):
#     model = Service
#     template_name = "services/delete_service.html"
#     permission_required = ("pages.delete_service",)
#     success_url = reverse_lazy("pages:list-service")
#     extra_context = {"title": "Delete Service"}
#     http_method_names = ["post"]


# views of Flatpages


class ListFlatPageView(PermissionRequiredMixin, ListView):
    model = FlatPage
    template_name = "flatpage/list_flatpage.html"
    permission_required = "pages.view_flatpage"
    context_object_name = "flatpages"
    extra_context = {"title": "FlatPages"}


class AddFlatPageView(PermissionRequiredMixin, CreateView):
    model = FlatPage
    form_class = FlatPageForm
    template_name = "flatpage/add_flatpage.html"
    permission_required = "pages.add_flatpage"
    success_url = reverse_lazy("pages:list-flatpage")
    success_message = '"%(title)s" added successfully!'
    extra_context = {"title": "Add Flatpage"}


class UpdateFlatPageView(PermissionRequiredMixin, UpdateView):
    model = FlatPage
    form_class = FlatPageForm
    template_name = "flatpage/update_flatpage.html"
    permission_required = "pages.change_flatpage"
    success_url = reverse_lazy("pages:list-flatpage")
    success_message = '"%(title)s" updated successfully!'
    extra_context = {"title": "Update Flatpage"}


class DeleteFlatPageView(PermissionRequiredMixin, DeleteView):
    model = FlatPage
    template_name = "flatpage/delete_flatpage.html"
    permission_required = "pages.delete_flatpage"
    success_url = reverse_lazy("pages:list-flatpage")
    extra_context = {"title": "Delete Flatpage"}
    http_method_names = ["post"]


# views of Ads


# class ListAdView(PermissionRequiredMixin, ListView):
#     model = Ad
#     template_name = "Ads/list_ads.html"
#     permission_required = "pages.view_ads"
#     context_object_name = "ads"
#     extra_context = {"title": "Ads"}


# class AddAdView(PermissionRequiredMixin, CreateView):
#     model = Ad
#     form_class = AdsForm
#     template_name = "Ads/add_ads.html"
#     permission_required = "pages.add_ads"
#     success_url = reverse_lazy("pages:list-ads")
#     success_message = '"%(title)s" added successfully'
#     extra_context = {"title": "Add Ads"}


# class UpdateAdView(PermissionRequiredMixin, UpdateView):
#     model = Ad
#     form_class = UpdateAdsForm
#     template_name = "Ads/update_ads.html"
#     permission_required = "pages.change_ads"
#     success_url = reverse_lazy("pages:list-ads")
#     success_message = '"%(title)s" updated successfully'
#     extra_context = {"title": "Update Ads"}


# class DeleteAdView(PermissionRequiredMixin, DeleteView):
#     model = Ad
#     template_name = "Ads/delete_ads.html"
#     permission_required = "pages.delete_ads"
#     success_url = reverse_lazy("pages:list-ads")
#     extra_context = {"title": "Delete Ads"}
#     http_method_names = ["post"]
