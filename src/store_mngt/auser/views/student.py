import imp

from django.contrib.admin.models import LogEntry
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from auser.forms import StudentRegistrationForm
from auser.mixins import LogEntryChangeMixin, LogEntryDeletionMixin
from auser.models import Student


class SignUpView(SuccessMessageMixin, CreateView):
    model = Student
    template_name = "auser/signup.html"
    form_class = StudentRegistrationForm
    success_url = reverse_lazy("auser:login")
    success_message = _("Your account was created successfully. Please login.")
    extra_context = {"title": _("Sign Up")}


class ListActiveStudentsView(PermissionRequiredMixin, ListView):
    model = Student
    template_name = "auser/student/list_active_students.html"
    permission_required = ("auser.view_student",)
    extra_context = {"title": _("Active Students")}
    context_object_name = "students"

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class ListDeactivatedStudentsView(PermissionRequiredMixin, ListView):
    model = Student
    template_name = "auser/student/list_deactivated_students.html"
    permission_required = ("auser.view_student",)
    extra_context = {"title": _("Deactivated Students")}
    context_object_name = "deactivated_students"

    def get_queryset(self):
        return self.model.objects.filter(is_active=False)


class ActivateStudentView(
    PermissionRequiredMixin, SuccessMessageMixin, LogEntryChangeMixin, UpdateView
):
    model = Student
    template_name = "auser/student/activate_student.html"
    fields = ("is_active",)
    permission_required = ("auser.activate_student",)
    success_url = reverse_lazy("auser:deactivated_student_list")
    success_message = _("%(first_name)s %(last_name)s activated successfully")
    http_method_names = ["post"]

    def form_valid(self, form):
        form.cleaned_data.update(
            {"first_name": self.object.first_name, "last_name": self.object.last_name}
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_active": True})
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def get_queryset(self):
        return self.model.objects.filter(is_active=False)


class DeactivateStudentView(
    PermissionRequiredMixin, SuccessMessageMixin, LogEntryChangeMixin, UpdateView
):
    model = Student
    template_name = "auser/student/deactivate_student.html"
    permission_required = ("auser.deactivate_student",)
    fields = ("is_active",)
    success_url = reverse_lazy("auser:active_student_list")
    success_message = _("%(first_name)s %(last_name)s deactivated successfully")
    http_method_names = ["post"]

    def form_valid(self, form):
        form.cleaned_data.update(
            {"first_name": self.object.first_name, "last_name": self.object.last_name}
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_data = form_kwargs.get("data", {}).copy()
        form_data.update({"is_active": False})
        form_kwargs.update({"data": form_data})
        return form_kwargs

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class DeleteStudentView(
    PermissionRequiredMixin, SuccessMessageMixin, LogEntryDeletionMixin, DeleteView
):
    model = Student
    template_name = "auser/student/confirm_delete_student.html"
    permission_required = (
        "auser.view_student",
        "auser.delete_student",
    )
    success_url = reverse_lazy("auser:deactivated_student_list")
    http_method_names = ["post"]

    def get_queryset(self):
        return self.model.objects.filter(is_active=False)


class StudentDetailView(PermissionRequiredMixin, DetailView):
    model = Student
    template_name = "auser/student/student_detail.html"
    extra_context = {"title": _("Student Detail")}
    permission_required = ("auser.view_student",)
    context_object_name = "student"

    def get_content_type(self):
        """Return content type for LogEntry"""

        return ContentType.objects.get_for_model(self.model).pk

    def get_object_hisotry(self):
        """Return log entries for the object"""

        return LogEntry.objects.filter(
            content_type_id=self.get_content_type(), object_id=self.object.pk
        )

    def get_context_data(self, **kwargs):
        kwargs.update(
            {
                "object_history": self.get_object_hisotry(),
            }
        )
        return super().get_context_data(**kwargs)
