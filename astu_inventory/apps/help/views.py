from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from django_summernote.fields import SummernoteTextFormField

from astu_inventory.apps.help.models import Help


class ListHelpsView(PermissionRequiredMixin, ListView):
    model = Help
    permission_required = "help.view_help"
    template_name = "help/list.html"
    context_object_name = "helps"
    extra_context = {"title": "Help"}


class UpdateHelpView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Help
    fields = ("content", "is_visible")
    template_name = "help/update.html"
    success_url = reverse_lazy("help:helps_list")
    permission_required = "help.change_help"
    success_message = "Help content updated successfully!"
    extra_context = {"title": "Update help"}

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form["content"].field = SummernoteTextFormField()
        return form
