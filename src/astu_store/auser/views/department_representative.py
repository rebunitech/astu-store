from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from auser.mixins import ActiveCollegeRequiredMixin, CreateUserMixin
from auser.models import CollegeUser
from auser.views.user import (ActivateUserView, DeactivateUserView,
                              DeleteUserView, UpdateUserView)


class DepartmentRepresentativesListView(PermissionRequiredMixin, ListView):
    model = CollegeUser
    context_object_name = "department_heads"
    permission_required = "can_view_department_representatives"
    template_name = "auser/department/representative/list.html"

    def get_queryset(self):
        qs = self.model.objects.filter(
            Q(college__short_name=self.kwargs["short_name"])
            & Q(department__short_name=self.kwargs["dept_short_name"])
            & Q(groups__name="department_representative")
        ).exclude(Q(groups__name="college_representative"))
        return qs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Heads of  {self.kwargs['dept_short_name']}"})
        return context_data


class AddDepartmentRepresentativeView(
    PermissionRequiredMixin,
    ActiveCollegeRequiredMixin,
    CreateUserMixin,
    SuccessMessageMixin,
    CreateView,
):
    model = CollegeUser
    fields = (
        "email",
        "sex",
        "phone_number",
    )
    permission_required = "auser.can_add_department_representative"
    user_object_name = "department head"
    groups = ["department_representative"]

    def get_success_url(self):
        return reverse_lazy(
            "auser:department_representatives",
            args=[self.kwargs["short_name"], self.kwargs["dept_short_name"]],
        )

    def form_valid(self, form):
        college_short_name = self.kwargs["short_name"]
        department_short_name = self.kwargs["dept_short_name"]
        self.object = form.save(commit=False)
        self.object.college = self.get_college(college_short_name)
        self.object.department = self.get_department(department_short_name)
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {"title": f"Add department head for {self.kwargs['dept_short_name']}"}
        )
        return context_data


class DepartmentRepresentativeUpdateView(UpdateUserView):
    fields = (
        "first_name",
        "last_name",
        "username",
        "email",
        "sex",
        "phone_number",
    )
    template_name = "auser/department/representative/update.html"
    permission_required = "auser.can_change_department_representative"
    success_message = "%(first_name)s %(last_name)s updated successfully."

    def get_success_url(self):
        return reverse_lazy(
            "auser:department_representatives",
            args=[self.kwargs["short_name"], self.kwargs["dept_short_name"]],
        )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(college__short_name=self.kwargs["short_name"])
                & Q(department__short_name=self.kwargs["dept_short_name"])
                & Q(groups__name="department_representative")
            )
            .exclude(Q(groups__name="college_representative"))
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Update {self.object.get_full_name()}"})
        return context_data


class DepartmentRepresentativeActivateView(ActivateUserView):
    permission_required = ("auser.can_change_department_representative",)
    success_message = "%(first_name)s %(last_name)s activated successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy(
            "auser:department_representatives",
            args=[self.kwargs["short_name"], self.kwargs["dept_short_name"]],
        )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(college__short_name=self.kwargs["short_name"])
                & Q(department__short_name=self.kwargs["dept_short_name"])
                & Q(groups__name="department_representative")
            )
            .exclude(Q(groups__name="college_representative"))
        )


class DepartmentRepresentativeDeactivateView(DeactivateUserView):
    permission_required = ("auser.can_change_department_representative",)
    success_message = "%(first_name)s %(last_name)s deactivated successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy(
            "auser:department_representatives",
            args=[self.kwargs["short_name"], self.kwargs["dept_short_name"]],
        )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(college__short_name=self.kwargs["short_name"])
                & Q(department__short_name=self.kwargs["dept_short_name"])
                & Q(groups__name="department_representative")
            )
            .exclude(Q(groups__name="college_representative"))
        )


class RemoveFromDepartmentRepresentativeView(
    PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = CollegeUser
    fields = ("groups",)
    permission_required = ("auser.can_remove_department_representative",)
    success_message = "%(first_name)s %(last_name)s successfully removed from deans."
    http_method_names = ["post"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(college__short_name=self.kwargs["short_name"])
                & Q(department__short_name=self.kwargs["dept_short_name"])
                & Q(groups__name="department_representative")
            )
            .exclude(Q(groups__name="college_representative"))
        )

    def get_success_url(self):
        return reverse_lazy(
            "auser:department_representatives",
            args=[self.kwargs["short_name"], self.kwargs["dept_short_name"]],
        )

    def form_valid(self, form):
        form.cleaned_data.update(
            {"first_name": self.object.first_name, "last_name": self.object.last_name}
        )
        self.object.groups.set(
            self.object.groups.exclude(
                Q(name="college_representative") | Q(name="department_representative")
            )
        )
        return super().form_valid(form)


class DepartmentRepresentativeDeleteView(DeleteUserView):
    permission_required = ("auser.can_delete_department_representative",)
    success_message = "%(first_name)s %(last_name)s delete successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy(
            "auser:department_representatives",
            args=[self.kwargs["short_name"], self.kwargs["dept_short_name"]],
        )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(college__short_name=self.kwargs["short_name"])
                & Q(department__short_name=self.kwargs["dept_short_name"])
                & Q(groups__name="department_representative")
            )
            .exclude(Q(groups__name="college_representative"))
        )


class AddDepartmentStaffMemberView(
    ActiveCollegeRequiredMixin,
    PermissionRequiredMixin,
    CreateUserMixin,
    SuccessMessageMixin,
    CreateView,
):
    model = CollegeUser
    fields = (
        "email",
        "sex",
        "phone_number",
    )
    hidden_fields = "college"
    permission_required = "auser.can_add_department_staff_member"
    groups = ["staff_member"]

    def get_success_url(self):
        return reverse_lazy(
            "auser:department_staffs_list",
            args=[self.kwargs["short_name"], self.kwargs["dept_short_name"]],
        )

    def get_success_message(self, *args, **kwargs):
        return f'Staff member "{self.object.username}" added successfully.'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.college = self.get_college(self.kwargs["short_name"])
        self.object.department = self.get_department(self.kwargs["dept_short_name"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {"title": f"Add staff member for {self.kwargs['dept_short_name']}"}
        )
        return context_data


class DepartmentStaffMembersListView(DepartmentRepresentativesListView):
    permission_required = "auser.can_view_department_staff_member"
    template_name = "auser/department/staff_member/list.html"
    context_object_name = "staff_members"

    def get_queryset(self):
        qs = self.model.objects.filter(
            Q(college__short_name=self.kwargs["short_name"])
            & Q(department__short_name=self.kwargs["dept_short_name"])
        ).exclude(
            Q(groups__name="college_representative")
            & Q(groups__name="department_representative")
        )
        return qs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {"title": f"Staff members of  {self.kwargs['dept_short_name']}"}
        )
        return context_data


class DepartmentStaffMemberUpdateView(UpdateUserView):
    fields = (
        "first_name",
        "last_name",
        "username",
        "email",
        "sex",
        "phone_number",
    )
    template_name = "auser/department/staff_member/update.html"
    permission_required = "auser.can_change_department_staff_member"
    success_message = "%(first_name)s %(last_name)s updated successfully."

    def get_success_url(self):
        return reverse_lazy(
            "auser:department_staffs_list",
            args=[self.kwargs["short_name"], self.kwargs["dept_short_name"]],
        )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(college__short_name=self.kwargs["short_name"])
                & Q(department__short_name=self.kwargs["dept_short_name"])
            )
            .exclude(
                Q(groups__name="college_representative")
                & Q(groups__name="department_representative")
            )
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Update {self.object.get_full_name()}"})
        return context_data


class DepartmentStaffMemberActivateView(ActivateUserView):
    permission_required = ("auser.can_change_department_staff_member",)
    success_message = "%(first_name)s %(last_name)s activated successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy(
            "auser:department_staffs_list",
            args=[self.kwargs["short_name"], self.kwargs["dept_short_name"]],
        )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(college__short_name=self.kwargs["short_name"])
                & Q(department__short_name=self.kwargs["dept_short_name"])
            )
            .exclude(
                Q(groups__name="college_representative")
                & Q(groups__name="department_representative")
            )
        )


class DepartmentStaffMemberDeactivateView(DeactivateUserView):
    permission_required = ("auser.can_change_department_staff_member",)
    success_message = "%(first_name)s %(last_name)s deactivated successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy(
            "auser:department_staffs_list",
            args=[self.kwargs["short_name"], self.kwargs["dept_short_name"]],
        )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(college__short_name=self.kwargs["short_name"])
                & Q(department__short_name=self.kwargs["dept_short_name"])
            )
            .exclude(
                Q(groups__name="college_representative")
                & Q(groups__name="department_representative")
            )
        )


class DepartmentStaffMemberDeleteView(DeleteUserView):
    permission_required = ("auser.can_delete_department_staff_member",)
    success_message = "%(first_name)s %(last_name)s delete successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy(
            "auser:department_staffs_list",
            args=[self.kwargs["short_name"], self.kwargs["dept_short_name"]],
        )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(college__short_name=self.kwargs["short_name"])
                & Q(department__short_name=self.kwargs["dept_short_name"])
            )
            .exclude(
                Q(groups__name="college_representative")
                & Q(groups__name="department_representative")
            )
        )
