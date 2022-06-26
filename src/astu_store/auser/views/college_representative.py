from django.contrib.auth.mixins import (
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (CreateView, FormView,
                                  ListView, UpdateView)

from auser.forms import (
                         AssignDeprtmentRepresentativeForm)
from auser.mixins import (ActiveCollegeRequiredMixin, AssignUserMixin,
                          CreateUserMixin)
from auser.models import CollegeUser, Department
from auser.views.user import (ActivateUserView, DeactivateUserView,
                              DeleteUserView, UpdateUserView)


class AddCollegeRepresentativeView(
    ActiveCollegeRequiredMixin,
    PermissionRequiredMixin,
    CreateUserMixin,
    SuccessMessageMixin,
    CreateView,
):
    model = CollegeUser
    fields = (
        "department",
        "email",
        "sex",
        "phone_number",
    )
    hidden_fields = "college"
    extra_context = {"title": "Add college dean"}
    permission_required = "auser.can_add_college_representative"
    groups = ["college_representative", "department_representative"]

    def get_success_url(self):
        return reverse_lazy(
            "auser:college_representatives", args=[self.kwargs["short_name"]]
        )

    def get_success_message(self, *args, **kwargs):
        return f'College dean "{self.object.username}" added successfully.'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.college = self.get_college(self.kwargs["short_name"])
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form["department"].field.queryset = Department.objects.filter(
            college__short_name=self.kwargs["short_name"], college__status="active"
        )
        return form


class AssignCollegeRepresentativeView(
    PermissionRequiredMixin, SuccessMessageMixin, AssignUserMixin, FormView
):
    form_class = AssignDeprtmentRepresentativeForm
    template_name = "auser/college/add.html"
    permission_required = ("auser.can_add_college_representative",)
    extra_context = {"title": "Assign college dean"}
    success_url = reverse_lazy("auser:list_colleges")

    def get_success_message(self, *args, **kwargs):
        return f'User "{self.user.username} successfully assign as "{self.kwargs["short_name"]}" dean.'

    def form_valid(self, form):
        self.user = self.get_user(form)
        self.user.college = self.get_college(form)
        groups = self.get_groups(
            ["college_representative", "department_representative"]
        )
        self.user.groups.set(groups)
        return super().form_valid(form)


class CollegeRepresentativesListView(PermissionRequiredMixin, ListView):
    model = CollegeUser
    context_object_name = "college_deans"
    permission_required = "can_view_college_representatives"
    template_name = "auser/college/representatives/list.html"

    def get_queryset(self):
        qs = self.model.objects.filter(
            Q(college__short_name=self.kwargs["short_name"])
            & Q(groups__name="college_representative")
        )
        return qs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Deans of  {self.kwargs['short_name']}"})
        return context_data


class CollegeRepresentativeUpdateView(UpdateUserView):
    fields = (
        "first_name",
        "last_name",
        "username",
        "email",
        "sex",
        "phone_number",
        "department",
    )
    template_name = "auser/college/representatives/update.html"
    permission_required = "auser.can_change_college_representative"
    success_message = "%(first_name)s %(last_name)s updated successfully."

    def get_success_url(self):
        return reverse_lazy(
            "auser:college_representatives", args=[self.kwargs["short_name"]]
        )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(college__short_name=self.kwargs["short_name"])
                & Q(groups__name="college_representative")
            )
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"title": f"Update {self.object.get_full_name()}"})
        return context_data

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form["department"].field.queryset = Department.objects.filter(
            college__short_name=self.kwargs["short_name"], college__status="active"
        )
        return form


class CollegeRepresentativeActivateView(ActivateUserView):
    permission_required = ("auser.can_change_college_representative",)
    success_message = "%(first_name)s %(last_name)s activated successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy(
            "auser:college_representatives", args=[self.kwargs["short_name"]]
        )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(college__short_name=self.kwargs["short_name"])
                & Q(groups__name="college_representative")
            )
        )


class CollegeRepresentativeDeactivateView(DeactivateUserView):
    permission_required = ("auser.can_change_college_representative",)
    success_message = "%(first_name)s %(last_name)s deactivated successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy(
            "auser:college_representatives", args=[self.kwargs["short_name"]]
        )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(college__short_name=self.kwargs["short_name"])
                & Q(groups__name="college_representative")
            )
        )


class RemoveFromCollegeRepresentativeView(
    PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = CollegeUser
    fields = ("groups",)
    permission_required = ("auser.can_remove_college_representative",)
    success_message = "%(first_name)s %(last_name)s successfully removed from deans."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy(
            "auser:college_representatives", args=[self.kwargs["short_name"]]
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


class CollegeRepresentativeDeleteView(DeleteUserView):
    permission_required = ("auser.can_remove_college_representative",)
    success_message = "%(first_name)s %(last_name)s delete successfully."
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy(
            "auser:college_representatives", args=[self.kwargs["short_name"]]
        )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                Q(college__short_name=self.kwargs["short_name"])
                & Q(groups__name="college_representative")
            )
        )
