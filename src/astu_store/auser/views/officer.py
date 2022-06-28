from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError, Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from auser.forms import CollegeForm
from auser.models import College, CollegeUser


class CollegeStoreOfficersListView(PermissionRequiredMixin, ListView):
    model = CollegeUser
    context_object_name = "store_officers"
    permission_required = "auser.can_view_college_store_officer"
    template_name = "auser/college/store_officer/list.html"

    def get_queryset(self):
        qs = self.model.objects.filter(
            Q(college__short_name=self.kwargs["short_name"])
            & Q(groups__name="store_officer")
        )
        return qs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {"title": f"Store officers of  {self.kwargs['short_name']}"}
        )
        return context_data


class CollegeLabAssistantsOfficersListView(PermissionRequiredMixin, ListView):
    model = CollegeUser
    context_object_name = "lab_assistants"
    permission_required = "auser.can_view_college_lab_assistant"
    template_name = "auser/college/lab_assistant/list.html"

    def get_queryset(self):
        qs = self.model.objects.filter(
            Q(college__short_name=self.kwargs["short_name"])
            & Q(groups__name="lab_assistant")
        )
        return qs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {"title": f"Store officers of  {self.kwargs['short_name']}"}
        )
        return context_data


class DepartmentStoreOfficersListView(PermissionRequiredMixin, ListView):
    model = CollegeUser
    context_object_name = "store_officers"
    permission_required = "auser.can_view_ddepartment_store_officer"
    template_name = "auser/department/store_officer/list.html"

    def get_queryset(self):
        qs = self.model.objects.filter(
            Q(college__short_name=self.kwargs["short_name"])
            & Q(department__short_name=self.kwargs["dept_short_name"])
            & Q(groups__name="store_officer")
        )
        return qs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {"title": f"Store officers of  {self.kwargs['dept_short_name']}"}
        )
        return context_data


class DepartmentLabAssistantsOfficersListView(PermissionRequiredMixin, ListView):
    model = CollegeUser
    context_object_name = "lab_assistants"
    permission_required = "auser.can_view_department_lab_assistant"
    template_name = "auser/department/lab_assistant/list.html"

    def get_queryset(self):
        qs = self.model.objects.filter(
            Q(college__short_name=self.kwargs["short_name"])
            & Q(department__short_name=self.kwargs["dept_short_name"])
            & Q(groups__name="lab_assistant")
        )
        return qs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {"title": f"Lab assistants of  {self.kwargs['dept_short_name']}"}
        )
        return context_data
