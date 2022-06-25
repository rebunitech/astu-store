from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from auser.mixins import (LogEntryAdditionMixin, LogEntryChangeMixin,
                          LogEntryDeletionMixin, SuperuserRequiredMixin)
from auser.utils import generate_username

from auser.models import School, SchoolHead
UserModel = get_user_model()

from auser.signals import staff_user_created



class AddSchoolHeadView(
                         SuccessMessageMixin,  SuperuserRequiredMixin, LogEntryAdditionMixin,
                         CreateView
                        ):
                        #  TODO: SuperuserRequiredMixin, LogEntryAdditionMixin,
    """Generic view used to add school head"""

    model = SchoolHead
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "school",
        "phone_number",
        "sex",
        "location",
        "po_box",
      
    )
    permission_required = ("auser.add_schoolhead")
    success_url = reverse_lazy("auser:active_school_head_list")
    success_message = _("%(first_name)s %(last_name)s added successfully")
    template_name = "auser/schoolHead/add_school_head.html"
    extra_context = {"title": _("Add School Dean")}

    def get_success_url(self):
        x = staff_user_created.send(
            sender=self.model, instance=self.object, created=True
        )
        return super().get_success_url()

    def form_valid(self, form):
        """Set staff user to True"""
        self.object = form.save(commit=False)
        self.object.username = generate_username()
        self.object.save()
        return super().form_valid(form)


class UpdateSchoolHeadView( SuperuserRequiredMixin, 
                            LogEntryChangeMixin,
                            SuccessMessageMixin,
                             UpdateView 
                             ):
    """Generic view used to update school head"""

    model = SchoolHead
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "school"
        "sex",
        "phone_number",
        "po_box",
        "location",
        "profile_picture",
        "bio", # TODO: for foriegn key --school
    )
    permission_required = ("auser.change_schoolhead")
    success_url = reverse_lazy("auser:active_school_head_list")
    success_message = _("%(first_name)s %(last_name)s updated successfully")
    template_name = "auser/schoolHead/update_school_head.html"
    extra_context = {"title": _("Update School Dean")}

    def get_queryset(self):
        """Return all school heads"""

        return self.model.objects.filter(
             is_active=True
        )

class ListActiveSchoolHeadsView( SuperuserRequiredMixin, ListView):
    """Generic view used to list all school heads"""

    model = SchoolHead
    template_name = "auser/schoolHead/list_active_school_head.html"
    context_object_name = "school_heads"
    extra_context = {"title": _("Active School Dean")}

    def get_queryset(self):
        """Return all school heads"""

        return self.model.objects.filter(
             is_active=True
        )



class SchoolHeadDetailView(SuperuserRequiredMixin, DetailView):
    model = SchoolHead
    template_name = "auser/schoolHead/school_head_detail.html"
    extra_context = {"title": _("School Dean Detail")}
    context_object_name = "school_head"

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

    def get_content_type(self):
        """Return content type for LogEntry"""

        return ContentType.objects.get_for_model(self.model).pk

    def get_object_hisotry(self):
        """Return log entries for the object"""

        return LogEntry.objects.filter(   LogEntryChangeMixin, content_type_id=self.get_content_type(), object_id=self.object.pk
        )

    def get_context_data(self, **kwargs):
        kwargs.update(
            {
                "object_history": self.get_object_hisotry(),
            }
        )
        return super().get_context_data(**kwargs)


class ListDeactivatedSchoolHeadsView(ListView):
    """ Generic view used to list all deactivate school head. """

    model = SchoolHead
    template_name = "auser/schoolHead/list_deactivate_school_head.html"
    context_object_name = "deactivated_school_heads"
    extra_context = {"title": _("Deactivated School Dean")}

    def get_queryset(self):
        """Return all deactivate school heads"""

        return self.model.objects.filter(
            is_active=False
        )



class ActivateSchoolHeadView( SuccessMessageMixin,  UpdateView
):
    """Generic view used to activate """

    model = SchoolHead
    fields = ("is_active",)
    success_url = reverse_lazy("auser:deactivated_school_head")
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
        """Return all deactivate staff users"""

        return self.model.objects.filter(
            is_active=False
        )


class DeactivateSchoolHeadView( SuperuserRequiredMixin, 
                                SuccessMessageMixin, 
                                LogEntryChangeMixin,
                                 UpdateView 
                                 ):
    """Generic view used to deactivate school head"""

    model = SchoolHead
    fields = ("is_active",)
    success_url = reverse_lazy("auser:active_school_head_list")
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
        """Return all staff users"""

        return self.model.objects.filter(
            is_active=True
        )


class DeleteSchoolHeadView( SuperuserRequiredMixin,
                             LogEntryDeletionMixin,
                             DeleteView):
    """Generic view used to delete school head"""

    model = SchoolHead
    success_url = reverse_lazy("auser:deactivated_school_head_list")
    http_method_names = ["post"]

    def get_queryset(self):
        """Return all deactivate school head. """
        return self.model.objects.filter(
            is_active=False
        )
