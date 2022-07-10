from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from astu_inventory.apps.auser.models import Department
from astu_inventory.apps.auser.views.department import UserModel
from astu_inventory.apps.inventory.forms import ShelfForm
from astu_inventory.apps.inventory.models import Shelf, Store
from django.contrib.auth import get_user_model
UserModel = get_user_model()

class AddShelfView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Shelf
    form_class = ShelfForm
    permission_required = ("inventory.add_shelf",)
    success_message = _("Shelf added successfully.")
    template_name = "inventory/store/shelf/add.html"
    extra_context = {"title": _("Add shelf")}

    def get_store(self):
        return get_object_or_404(Store, pk=self.kwargs.get("pk"))

    def form_valid(self, form):
        form.instance.store = self.get_store()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "inventory:shelves_list", kwargs={"pk": self.kwargs.get("pk")}
        )


class ListShelvesView(PermissionRequiredMixin, ListView):
    model = Shelf
    permission_required = ("inventory.view_shelf",)
    context_object_name = "shelves"
    template_name = "inventory/store/shelf/list.html"
    extra_context = {"title": _("Shelves")}

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset().filter(store__pk=self.kwargs.get("pk"))
        if not user.is_college_user:
            return qs
        if user.is_college_representative:
            return qs.filter(Q(store__department__college=user.collegeuser.college))
        return qs.filter(Q(store__department=user.collegeuser.department))


class UpdateShelfView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Shelf
    form_class = ShelfForm
    permission_required = ("inventory.change_shelf",)
    success_message = _("Shelf updated successfully.")
    template_name = "inventory/store/shelf/update.html"
    extra_context = {"title": _("Update shelf")}
    slug_field = "shelf_id"
    slug_url_kwarg = "shelf_id"

    def get_success_url(self):
        return reverse_lazy(
            "inventory:shelves_list", kwargs={"pk": self.kwargs.get("pk")}
        )

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset().filter(store__pk=self.kwargs.get("pk"))
        if not user.is_college_user:
            return qs
        if user.is_college_representative:
            return qs.filter(Q(store__department__college=user.collegeuser.college))
        return qs.filter(Q(store__department=user.collegeuser.department))


class DeleteShelfView(PermissionRequiredMixin, DeleteView):
    model = Shelf
    permission_required = ("store.delete_shelf",)
    slug_field = "shelf_id"
    slug_url_kwarg = "shelf_id"
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy(
            "inventory:shelves_list", kwargs={"pk": self.kwargs.get("pk")}
        )

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset().filter(store__pk=self.kwargs.get("pk"))
        if not user.is_college_user:
            return qs
        if user.is_college_representative:
            return qs.filter(Q(store__department__college=user.collegeuser.college))
        return qs.filter(Q(store__department=user.collegeuser.department))
