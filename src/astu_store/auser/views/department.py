from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from auser.forms import DepartmentForm
from auser.models import College, Department


class ListDepartmentsOfCollegeView(PermissionRequiredMixin, ListView):
    model = Department
    permission_required = (
        "auser.add_college",
        "auser.view_college",
        "auser.view_department",
        "auser.add_department",
    )
    context_object_name = "departments"
    template_name = "auser/department/list.html"

    def get_queryset(self):
        college = get_object_or_404(College, short_name=self.kwargs.get("short_name"))
        return super().get_queryset().filter(Q(college=college))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {"title": f"Departments of {self.kwargs.get('short_name')}"}
        )
        return context_data


class DepartmentDetailView(PermissionRequiredMixin, DetailView):
    model = Department
    template_name = "auser/department/detail.html"
    slug_field = "short_name"
    slug_url_kwarg = "dept_short_name"
    permission_required = "view_department"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"{self.object.short_name}", "title_only": True})
        return context_data

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(college__short_name=self.kwargs["short_name"]))
        )


class AddDepartmentView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    permission_required = ("auser.add_department",)
    success_message = _('Department "%(short_name)s" added successfully.')
    template_name = "auser/department/add.html"

    def get_success_url(self):
        return reverse_lazy(
            "auser:list_departments_for_college", args=[self.kwargs["short_name"]]
        )

    def form_valid(self, form):
        form.instance.college = get_object_or_404(
            College, short_name=self.kwargs.get("short_name")
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {"title": f"Add department for {self.kwargs.get('short_name')}"}
        )
        return context_data


class UpdateDepartmentView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    permission_required = ("auser.change_college",)
    success_message = _('Department "%(short_name)s" updated successfully.')
    template_name = "auser/department/update.html"
    slug_field = "short_name"
    slug_url_kwarg = "dept_short_name"

    def get_success_url(self):
        return reverse_lazy(
            "auser:list_departments_for_college", args=[self.kwargs["short_name"]]
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Update {self.object.short_name}"})
        return context_data

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(college__short_name=self.kwargs["short_name"]))
        )


class ActivateDepartmentView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Department
    fields = ("status",)
    permission_required = ("auser.can_change_department",)
    success_message = _('Department "%(short_name)s" activated successfully.')
    http_method_names = ["post"]
    slug_field = "short_name"
    slug_url_kwarg = "dept_short_name"

    def get_success_url(self):
        return reverse_lazy(
            "auser:list_departments_for_college", args=[self.kwargs["short_name"]]
        )

    def form_valid(self, form):
        form.cleaned_data.update({"short_name": self.object.short_name})
        return super().form_valid(form)

    def get_queryset(self):
        return self.model.objects.filter(
            Q(status="deactivated") & Q(college__short_name=self.kwargs["short_name"])
        )

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"status": "active"})
        form_kwargs.update({"data": form_data})
        return form_kwargs


class DeactivateDepartmentView(
    PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Department
    fields = ("status",)
    permission_required = ("auser.can_change_department",)
    success_message = _('Department "%(short_name)s" deactivated successfully.')
    http_method_names = ["post"]
    slug_field = "short_name"
    slug_url_kwarg = "dept_short_name"

    def get_success_url(self):
        return reverse_lazy(
            "auser:list_departments_for_college", args=[self.kwargs["short_name"]]
        )

    def form_valid(self, form):
        form.cleaned_data.update({"short_name": self.object.short_name})
        return super().form_valid(form)

    def get_queryset(self):
        print(self.model.objects.filter())
        return self.model.objects.filter(
            Q(status="active") & Q(college__short_name=self.kwargs["short_name"])
        )

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"status": "deactivated"})
        form_kwargs.update({"data": form_data})
        return form_kwargs


class DeleteDepartmentView(PermissionRequiredMixin, DeleteView):
    model = Department
    permission_required = ("auser.delete_department",)
    http_method_names = ["post"]
    slug_field = "short_name"
    slug_url_kwarg = "dept_short_name"

    def get_success_url(self):
        return reverse_lazy(
            "auser:list_departments_for_college", args=[self.kwargs["short_name"]]
        )

    def get_queryset(self):
        return self.model.objects.filter(
            Q(college__short_name=self.kwargs["short_name"])
        )

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as error:
            messages.error(
                request,
                f"You cann't delete this college, because there is {len(error.protected_objects)} related departemnts and/or staff members for this college. try to delete related objects first.",
            )
            return HttpResponseRedirect(
                reverse_lazy(
                    "auser:department_detail",
                    args=[self.kwargs["short_name"], self.kwargs["dept_short_name"]],
                )
            )


class ListDepartmentsOfCollegeView(PermissionRequiredMixin, ListView):
    model = Department
    permission_required = (
        "auser.add_college",
        "auser.view_college",
        "auser.view_department",
        "auser.add_department",
    )
    context_object_name = "departments"
    template_name = "auser/department/list.html"

    def get_queryset(self):
        college = get_object_or_404(College, short_name=self.kwargs.get("short_name"))
        return super().get_queryset().filter(Q(college=college))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {"title": f"Departments of {self.kwargs.get('short_name')}"}
        )
        return context_data
