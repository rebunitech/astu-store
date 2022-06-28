from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from inventory.models import Measurment, SpecificationType


class AddSpecificationTypeView(
    PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    model = SpecificationType
    fields = (
        "name",
        "si_unit",
    )
    permission_required = ("inventory.add_specificationtype",)
    success_message = _('Specification type "%(name)s" added successfully.')
    template_name = "inventory/specification/type/add.html"
    success_url = reverse_lazy("inventory:specification_types_list")
    extra_context = {"title": _("Add specification type")}


class ListSpecificationTypesView(PermissionRequiredMixin, ListView):
    model = SpecificationType
    permission_required = ("inventory.view_specificationtype",)
    context_object_name = "specification_types"
    template_name = "inventory/specification/type/list.html"
    extra_context = {"title": _("Specification Types")}


class UpdateSpecificationTypeView(
    PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = SpecificationType
    fields = ("name", "si_unit")
    permission_required = ("inventory.change_specificationtype",)
    success_message = _('Specification type "%(name)s" updated successfully.')
    template_name = "inventory/specification/type/update.html"
    success_url = reverse_lazy("inventory:specification_types_list")
    extra_context = {"title": _("Update specification type")}


class DeleteSpecificationTypeView(PermissionRequiredMixin, DeleteView):
    model = SpecificationType
    permission_required = ("inventory.delete_specificationtype",)
    success_url = reverse_lazy("inventory:specification_types_list")
    http_method_names = ["post"]


class AddMeasurmentView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Measurment
    fields = ("name",)
    permission_required = ("inventory.add_measurment",)
    success_message = _('Measurment "%(name)s" added successfully.')
    template_name = "inventory/measurment/add.html"
    success_url = reverse_lazy("inventory:measurments_list")
    extra_context = {"title": _("Add Measurment")}


class ListMeasurmentsView(PermissionRequiredMixin, ListView):
    model = Measurment
    permission_required = ("inventory.view_measurment",)
    context_object_name = "measurments"
    template_name = "inventory/measurment/list.html"
    extra_context = {"title": _("Measurment")}


class UpdateMeasurmentView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Measurment
    fields = ("name",)
    permission_required = ("inventory.change_measurment",)
    success_message = _('Measurment "%(name)s" updated successfully.')
    template_name = "inventory/measurment/update.html"
    success_url = reverse_lazy("inventory:measurments_list")
    extra_context = {"title": _("Update Measurment")}


class DeleteMeasurmentView(PermissionRequiredMixin, DeleteView):
    model = Measurment
    permission_required = ("inventory.delete_measurment",)
    success_url = reverse_lazy("inventory:measurments_list")
    http_method_names = ["post"]
