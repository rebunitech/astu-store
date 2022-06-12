
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ( CreateView, UpdateView,
                                    DeleteView, DetailView, ListView) 

from auser.models import Department

from auser.utils import generate_username

class AddDepartmentView(CreateView, SuccessMessageMixin, PermissionRequiredMixin):
    """Generic view used to add department. """

    model = Department
    fields = (
        "name",
        "abbr_name",
        "school",
        "email",
        "phone_number",
        "location",
        "po_box",
    )

    permission_required = ("auser.add_department",)
    template_name = "auser/department/add_department.html"
    success_message = _("%(name)s department is added successfully")
    success_url = reverse_lazy("auser:active_department_list")
    extra_context = {"title": _("Add Department")}
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = generate_username()
        self.object.save()

        return super().form_valid(form)


class UpdateDepartmentView(UpdateView, PermissionRequiredMixin, SuccessMessageMixin):
    """ Generic view to update view of department. """

    model = Department
    fields = (
        "name",
        "abbr_name",
        "school",
        "email",
        "phone_number",
        "location",
        "po_box",        
    )

    permission_required = ("auser.change_department",)
    template_name: str = "auser/department/update_department.html"
    success_url  = reverse_lazy("auser:active_department_list") 
    success_message: str = _("%(name)s department is updated successfully")
    extra_context = {"title": _("Update Department")}
    conext_object_name: str = "department"

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class ListActiveDepartmentView(PermissionRequiredMixin, ListView):
    """ Generic view used to view all lists of department. """

    model = Department
    template_name: str = "auser/department/list_active_department.html"
    permission_required: str = "auser.view_department"
    extra_context = {"title": _("List of Active Departments")}
    context_object_name: str = "departments"
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class ListDeactiveDepartmentView(PermissionRequiredMixin, ListView):
    """ Generic view to list all deactivate department. """

    model = Department
    template_name= "auser/department/list_deactive_department.html"
    permission_required = "auser:view_department"
    extra_context = {"title": _("List of Deactive Departments")}
    context_object_name = "departments"
    paginate_by: int = 10

    def get_queryset(self):
        return self.model.objects.filter(is_active=False)

class DepartmentDetailView(DetailView, PermissionRequiredMixin):
    """ Generic view to view details of a department.Detail  """

    model = Department
    template_name = "auser/department/department_detail.html"
    permission_required = "auser.view_department"
    context_object_name = "department"
    extra_context = {"title": _("Department Details")}

    
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


class DeleteDepartment(PermissionRequiredMixin, DeleteView):
    """ to delete department"""

    model = Department
    permission_required = "auser.delete_department"
    success_url = reverse_lazy("auser:list_deactivate_department")
    http_method_names = ["post"]

    def get_queryset(self) :
        return self.model.objects.filter(is_active=False)



class DeactivateDepartmentView(
                                     PermissionRequiredMixin, 
                                     SuccessMessageMixin, UpdateView
                                    ):
    """Generic view used to deactivate department. """

    model = Department
    fields = ("is_active",)
    permission_required = ("auser.deactivate_department",)
    success_url = reverse_lazy("auser:active_department_list")
    success_message = _("%(name)s %(abbr_name)s deactivated successfully")
    http_method_names = ["post"]

    def form_valid(self, form):
        form.cleaned_data.update(
            {"name": self.object.name, "abbr_name": self.object.abbr_name}
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


class ActivateDepartmentView(
                                  PermissionRequiredMixin, 
                                  SuccessMessageMixin, UpdateView 
                                  ):
    """Generic view used to activate department """

    model = Department
    fields = ("is_active",)
    permission_required = ("auser.activate_department",)
    success_url = reverse_lazy("auser:active_department_list")
    success_message = _("%(first_name)s %(last_name)s activated successfully")
    http_method_names = ["post"]

    def form_valid(self, form):
        form.cleaned_data.update(
            {"name": self.object.name, "abbr__name": self.object.abbr_name}
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
