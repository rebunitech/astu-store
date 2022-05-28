from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)

from auser.mixins import CreateUserMixin
from auser.models import College


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "auser/dashboard.html"
    extra_context = {"title": _("Dashboard")}


class ListCollegesView(PermissionRequiredMixin, ListView):
    model = College
    permission_required = ("college.view_college",)
    context_object_name = "colleges"
    template_name = "auser/college/list.html"
    extra_context = {"title": _("Colleges")}


class AddCollegeView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = College
    fields = (
        "name",
        "short_name",
        "description",
    )
    permission_required = ("auser.add_college",)
    success_message = _('College "%(short_name)s" added successfully.')
    template_name = "auser/college/add.html"
    success_url = reverse_lazy("auser:list_colleges")
    extra_context = {"title": _("Add College")}


class UpdateCollegeView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = College
    fields = ("name", "short_name", "description", "status")
    permission_required = ("auser.change_college",)
    success_message = _('College "%(short_name)s" updated successfully.')
    template_name = "auser/college/update.html"
    success_url = reverse_lazy("auser:list_colleges")
    slug_field = "short_name"
    slug_url_kwarg = "short_name"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Update {self.object.short_name}"})
        return context_data


class DeleteCollegeView(PermissionRequiredMixin, DeleteView):
    model = College
    permission_required = ("auser.delete_college",)
    success_url = reverse_lazy("auser:list_colleges")
    http_method_names = ["post"]
    slug_field = "short_name"
    slug_url_kwarg = "short_name"


class AddCollegeRepresentativeView(CreateUserMixin):
    permission_required = "auser.add_collegerepresentative"
    user_object_name = "college representative"
    groups = ["college_representative"]
