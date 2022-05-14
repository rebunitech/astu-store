from django.contrib.admin.models import LogEntry
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from auser.models import DepartmentHead

from auser.utils import generate_username


class AddDepartmenHead(CreateView, SuccessMessageMixin, PermissionRequiredMixin):
    """Generic view used to add content creator"""

    model = DepartmentHead
    fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "sex",
        "location",
        "po_box",
    )
    permission_required = ("auser.add_departmenthead",)
    template_name = "auser/departmentHead/add_department_head.html"
    success_message = _("%(first_name)s %(last_name)s added successfully")
    # success_url = reverse_lazy("auser:active_department_head_list")
    extra_context = {"title": _("Add Content Creator")}
    def form_valid(self, form):
            self.object = form.save(commit=False)
            self.object.username = generate_username()
            self.object.save()
            return super().form_valid(form)
