# from msilib.schema import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import ( DeleteView, UpdateView,
                                    CreateView, DetailView, ListView)

from django.urls import reverse_lazy
from auser.utils import generate_username

from auser.models import School

class AddSchoolView(PermissionRequiredMixin, CreateView):
    """ Generic view used to add school. """

    model = School
    fields = (
        "name",
        "abbr_name",
        "email",
        "phone_number",
        "location",
        "po_box",
    )

    permission_required = "auser.add_school"
    template_name = "auser/school/add_school.html"
    success_message = _("%(name)s School is added successfully")
    success_url = reverse_lazy("auser:active_school_list")
    extra_context = {"title": _("Add School")}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = generate_username()
        self.object.save()

        return super().form_valid(form)


class UpdateSchoolView(PermissionRequiredMixin, UpdateView):
    """ ... """

    model = School
    fields = (
        "name",
        "abbr_name",
        "location",
        "phone_number",
        "email",
        "po_box",
    )
    permission_required = "auser.change_school"
    template_name = "auser/school/update_school.html"
    success_url = reverse_lazy("auser:active_school_list")
    success_message = _("%(name)s School is updated successfully")
    extra_context = {"title": _("Update School")}
    context_object_name = "schools"


    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

class ListActiveSchoolView(PermissionRequiredMixin, ListView):
    """ ... """

    model = School
    permission_required = "auser.view_school"
    template_name = "auser/school/active_school_list.html"
    context_object_name = "schools"
    paginate_by: int = 10
    extra_context= {"title": _("Active School List")}

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

class ListDeactivatedSchoolView(PermissionRequiredMixin, ListView):
    """ ... """

    model = School
    permission_required = "auser.view_school"
    template_name = "auser/school/deactivated_school_list.html"
    context_object_name = "schools"
    paginate_by: int = 10
    extra_context= {"title": _("Deactivated School List")}

    def get_queryset(self):
        return self.model.objects.filter(is_active=False)

class SchoolDetailView(PermissionRequiredMixin, DetailView):
    """ ... """

    model = School
    template_name = "auser/school/school_detail.html"
    permission_required = "auser.view_school"
    context_object_name = "school"
    extra_context = {"title": _("School Details ")}

    def get_content_type(self):
        """ Get content type of the model for logentry. """
        return ContentType.objects.get_for_model(self.model).pk

    def get_object_history(self):
        """ Get object history of the model. """
        return LogEntry.objects.filter(
            content_type=self.get_content_type(),
            object_id=self.object.pk
        )

    def get_context_data(self, **kwargs):
        kwargs.update(
            {
                "object_history": self.get_object_history(),
            }
        )
        return super().get_context_data(**kwargs)    

class DeactivateSchoolView( PermissionRequiredMixin, 
                                     SuccessMessageMixin, UpdateView
                                    ):
    """Generic view used to deactivate school"""

    model = School
    fields = ("is_active",)
    permission_required = ("auser.deactivate_school",)
    success_url = reverse_lazy("auser:active_school_list")
    success_message = _("%(first_name)s %(last_name)s deactivated successfully")
    http_method_names = ["post"]

    def form_valid(self, form):
        form.cleaned_data.update(
            {"first_name": self.object.abbr_name,}
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

class ActivateSchoolView( PermissionRequiredMixin, 
                                     SuccessMessageMixin, UpdateView
                                    ):
    """Generic view used to activate school"""

    model = School
    fields = ("is_active",)
    permission_required = ("auser.activate_school",)
    success_url = reverse_lazy("auser:deactivated_school_list")
    success_message = _("%(first_name)s %(last_name)s activated successfully")
    http_method_names = ["post"]

    def form_valid(self, form):
        form.cleaned_data.update(
            {"first_name": self.object.abbr_name,}
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

class DeleteSchool(PermissionRequiredMixin, DeleteView):
    """ ... """
    model = School
    permission_required = "auser.delete_school"
    success_url = reverse_lazy("auser:active_school_list")
    success_message = _("%(name)s School is deleted successfully")
    http_method_names = ["post"]
    
    def get_queryset(self):
        return self.model.objects.filter(is_active=False)