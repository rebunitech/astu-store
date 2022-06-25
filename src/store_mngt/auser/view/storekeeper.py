from django.contrib.admin.models import LogEntry
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from auser.models import Storekeeper
from auser.utils import generate_username
from auser.mixins import ( CurrentUserMixin, LogEntryChangeMixin,
                           LogEntryDeletionMixin, LogEntryAdditionMixin )


class AddStoreKeeper(CreateView, SuccessMessageMixin, PermissionRequiredMixin):
    """Generic view used to add store keeper. """

    model = Storekeeper
    fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "sex",
        "location",
        "po_box",
        "department",
    )
    permission_required = ("auser.add_storekeeper",)  #TODO:
    template_name = "auser/storekeeper/add_store_keeper.html"
    success_message = _("%(first_name)s %(last_name)s added successfully")
    success_url = reverse_lazy("auser:active_store_keeper_list")
    extra_context = {"title": _("Add Store Officer")}
    
    def form_valid(self, form):
            self.object = form.save(commit=False)
            self.object.username = generate_username()
            self.object.save()
            return super().form_valid(form)

class UpdateStoreKeeper( PermissionRequiredMixin, 
                            SuccessMessageMixin, UpdateView 
                            ):
    """Generic view used to update store keeper. """

    model = Storekeeper
    fields = (
        "first_name",
        "last_name",
        "username",
        "email",
        "phone_number",
        "sex",
        "location",
        "po_box",
        "profile_picture",
        "bio",
    )
    permission_required = ("auser.change_storekeeper",)
    success_url = reverse_lazy("auser:active_store_keeper_list")
    template_name = "auser/storekeeper/update_store_keeper.html"
    success_message = _("%(first_name)s %(last_name)s updated successfully")
    extra_context = {"title": _("Update Store Officer")}

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class ListActiveStoreKeepersView(PermissionRequiredMixin, ListView):
    model = Storekeeper
    template_name = "auser/storekeeper/list_store_keepers.html"
    permission_required = ("auser.view_store_keeper",)
    extra_context = {"title": _("Active Store Officer")}
    context_object_name = "storekeepers"

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

class ListDeactivatedStoreKeepersView(PermissionRequiredMixin, ListView):
    model = Storekeeper
    template_name = "auser/storekeeper/list_deactivated_store_keeper.html"
    permission_required = ("auser.view_storekeeper",)
    extra_context = {"title": _("Deactivated Store Officer")}
    context_object_name = "deactivated_store_keepers"

    def get_queryset(self):
        return self.model.objects.filter(is_active=False)


class ActivateStoreKeeperView(
                             PermissionRequiredMixin,
                              SuccessMessageMixin,
                              LogEntryChangeMixin,
                               UpdateView ):
    model = Storekeeper
    fields = ("is_active",)
    permission_required = ("auser.activate_store_keeper",)
    success_url = reverse_lazy("auser:deactivated_store_keeper_list")
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


class DeactivateStoreKeeperView(
                             PermissionRequiredMixin,
                              SuccessMessageMixin,
                              LogEntryChangeMixin,
                               UpdateView ):
    model = Storekeeper
    permission_required = ("auser.deactivate_store_keeper",)
    fields = ("is_active",)
    success_url = reverse_lazy("auser:active_store_keeper_list")
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



class DeleteStoreKeeprView(
                            PermissionRequiredMixin,
                             SuccessMessageMixin,
                             LogEntryDeletionMixin,
                              DeleteView  ):
    model = Storekeeper
    permission_required = ( 
        "auser.view_storekeeper",
        "auser.delete_storekeeper",
    )
    success_url = reverse_lazy("auser:deactivated_store_keeper_list")
    http_method_names = ["post"]

    def get_queryset(self):
        return self.model.objects.filter(is_active=False)



class StoreKeeperDetailView(PermissionRequiredMixin, DetailView):
    model = Storekeeper
    template_name = "auser/storekeeper/store_keeper_detail.html"
    extra_context = {"title": _("Store Officer Detail")}
    permission_required = ("auser.view_store_keeper",)
    context_object_name = "storekeeper"

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
