from django.contrib.auth.mixins import (
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView)

from auser.models import College


class ListCollegesView(PermissionRequiredMixin, ListView):
    model = College
    permission_required = ("auser.view_college", "auser.add_college")
    context_object_name = "colleges"
    template_name = "auser/college/list.html"
    extra_context = {"title": _("Colleges"), "help_index": "add_staff"}


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
    extra_context = {"title": _("Add College")}

    def get_success_url(self):
        return reverse_lazy("auser:college_detail", args=[self.kwargs["short_name"]])


class CollegeDetailView(PermissionRequiredMixin, DetailView):
    model = College
    template_name = "auser/college/detail.html"
    slug_field = "short_name"
    slug_url_kwarg = "short_name"
    permission_required = "view_college"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"{self.object.short_name}", "title_only": True})
        return context_data


class UpdateCollegeView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = College
    fields = (
        "name",
        "short_name",
        "description",
    )
    permission_required = ("auser.change_college",)
    success_message = _('College "%(short_name)s" updated successfully.')
    template_name = "auser/college/update.html"
    slug_field = "short_name"
    slug_url_kwarg = "short_name"

    def get_success_url(self):
        return reverse_lazy("auser:college_detail", args=[self.kwargs["short_name"]])

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


class ActivateCollegeView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = College
    fields = ("status",)
    permission_required = ("auser.can_change_college",)
    success_message = _('College "%(short_name)s" activated successfully.')
    http_method_names = ["post"]
    slug_field = "short_name"
    slug_url_kwarg = "short_name"

    def get_success_url(self):
        return reverse_lazy("auser:college_detail", args=[self.kwargs["short_name"]])

    def form_valid(self, form):
        form.cleaned_data.update({"short_name": self.kwargs["short_name"]})
        return super().form_valid(form)

    def get_queryset(self):
        return self.model.objects.filter(Q(status="deactivated"))

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"status": "active"})
        form_kwargs.update({"data": form_data})
        return form_kwargs


class DeactivateCollegeView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = College
    fields = ("status",)
    permission_required = ("auser.can_change_college",)
    success_message = _('College "%(short_name)s" deactivated successfully.')
    http_method_names = ["post"]
    slug_field = "short_name"
    slug_url_kwarg = "short_name"

    def get_success_url(self):
        return reverse_lazy("auser:college_detail", args=[self.kwargs["short_name"]])

    def form_valid(self, form):
        form.cleaned_data.update({"short_name": self.kwargs["short_name"]})
        return super().form_valid(form)

    def get_queryset(self):
        return self.model.objects.filter(Q(status="active"))

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"status": "deactivated"})
        form_kwargs.update({"data": form_data})
        return form_kwargs
