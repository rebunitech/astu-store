"""ASTU Inventory auser views

Each class represents a logic layer of the project, related to department.

    Date Created: 14 July, 2022
    Author: Ashenafi Zenebe
"""

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ( CreateView, UpdateView,
                                    DeleteView, ListView,
                                    FormView, )
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import ProtectedError, Q

from astu_inventory.apps.auser.models import User
from astu_inventory.apps.auser.views.department import UserModel

UserModel = get_user_model()


class AllStaffMemberListView(PermissionRequiredMixin, ListView, SuccessMessageMixin):
    """ Lists of staff member form all the system. """

    model = UserModel
    template_name= "auser/staff_member/all/list.html"
    permission_required = "auser.can_list_staff_members"
    context_object_name = "staff_members"
    extra_context = {"title": "All Staff Members List"}

    def get_queryset(self):
        print("*(*(")
        return super().get_queryset().filter(Q(groups__name="staff member")).exclude(Q(groups__name="college dean"))

        # print (1234321)


class StaffMemberListView(ListView, PermissionRequiredMixin, SuccessMessageMixin):
    """ Lists of staff members for specific department. """

    model = UserModel
    template_name = "auser/staff_member/list.html"
    permission_requeried = "auser.can_list_staff_member"
    context_object_name = "staff_members"

    def get_queryset(self):
        return (
            super().get_queryset()
            .filter(Q(groups__name="staff member") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean") | Q(groups__name="department head"))
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"{self.kwargs['short_name'].upper()} staff members."})
        return context_data


class AllAddStaffMemberView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """ Add staff member to the system. """

    model = UserModel
    fields = (
        "department",
        "staff_id",
        "email",
        "sex",
        "phone_number",
    )
    template_name= "auser/staff_member/all/add.html"
    permission_required = "auser.can_add_staff_member"
    extra_context = {"title": "Add Staff Member"}
    success_message = _("Staff Member successfully added to the system ")
    success_url = "auser:all_staff_member_list"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.groups.add(Group.objects.get(name="staff member"))
        return response


class AllUpdateStaffMemberView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """Change existing staff member profile."""

    model = UserModel
    fields = (
        "staff_id",
        "department",
        "first_name",
        "last_name",
        "email",
        "sex",
        "phone_number",
        "location",
        "po_box",
        "profile_picture",
    )
    success_url = reverse_lazy("auser:all_staff_member_list")
    template_name = "auser/staff_member/all/update.html"
    permission_required = "auser.can_change_staff_member"
    success_message = "%(first_name)s %(last_name)s updated successfully."

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(groups__name="staff member") & Q(department__short_name__iexact=self.kwargs["short_name"]))
            .exclude(Q(groups__name="college dean"))
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Update {self.object.get_full_name()}"})
        return context_data


