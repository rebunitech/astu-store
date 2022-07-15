from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from astu_inventory.apps.inventory.forms import (
    AddItemSpecificationForm,
    AddProductSpecificationForm,
    UpdateItemSpecificationForm,
    UpdateProductSpecificationForm,
)
from astu_inventory.apps.inventory.models import Item, Measurment, Product, Specification, SpecificationType


class AddSpecificationTypeView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
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


class UpdateSpecificationTypeView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
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


class AddItemSpecificationView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Specification
    form_class = AddItemSpecificationForm
    permission_required = ("inventory.add_specification",)
    success_message = _("Specification added successfully.")
    template_name = "inventory/item/specification/add.html"
    extra_context = {"title": _("Add specification")}

    def get_initial(self):
        return self.kwargs

    def get_success_url(self):
        return reverse_lazy(
            "inventory:item_specifications_list",
            kwargs={"pk": self.kwargs.get("pk")},
        )


class ListItemSpecificationsView(PermissionRequiredMixin, ListView):
    model = Specification
    permission_required = ("inventory.view_specification",)
    context_object_name = "specifications"
    template_name = "inventory/item/specification/list.html"
    extra_context = {"title": _("Specifications")}

    def get_queryset(self):
        return super().get_queryset().filter(item__pk=self.kwargs.get("pk"))


class UpdateItemSpecificationView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Specification
    form_class = UpdateItemSpecificationForm
    permission_required = ("inventory.change_specification",)
    success_message = _("Specification updated successfully.")
    template_name = "inventory/item/specification/update.html"
    extra_context = {"title": _("Update item specification")}
    pk_url_kwarg = "s_pk"

    def get_initial(self):
        return self.kwargs

    def get_success_url(self):
        return reverse_lazy(
            "inventory:item_specifications_list",
            kwargs={"pk": self.object.item.pk},
        )


class DeleteItemSpecificationView(PermissionRequiredMixin, DeleteView):
    model = Specification
    permission_required = ("inventory.delete_specification",)
    http_method_names = ["post"]
    pk_url_kwarg = "s_pk"

    def get_success_url(self):
        return reverse_lazy(
            "inventory:item_specifications_list",
            kwargs={"pk": self.object.item.pk},
        )


class AddProductSpecificationView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Specification
    form_class = AddProductSpecificationForm
    permission_required = ("inventory.add_specification",)
    success_message = _("Specification added successfully.")
    template_name = "inventory/product/specification/add.html"
    extra_context = {"title": _("Add specification")}

    def get_initial(self):
        return self.kwargs

    def get_success_url(self):
        return reverse_lazy(
            "inventory:product_specifications_list",
            kwargs=self.kwargs,
        )


class ListProductSpecificationsView(PermissionRequiredMixin, ListView):
    model = Specification
    permission_required = ("inventory.view_specification",)
    context_object_name = "specifications"
    template_name = "inventory/product/specification/list.html"
    extra_context = {"title": _("Specifications")}

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                product__slug=self.kwargs.get("slug"),
                product__department__short_name__iexact=self.kwargs["short_name"],
            )
        )


class UpdateProductSpecificationView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Specification
    form_class = UpdateProductSpecificationForm
    permission_required = ("inventory.change_specification",)
    success_message = _("Specification updated successfully.")
    template_name = "inventory/product/specification/update.html"
    extra_context = {"title": _("Update product specification")}
    pk_url_kwarg = "s_pk"

    def get_success_url(self):
        self.kwargs.pop("s_pk")
        return reverse_lazy(
            "inventory:product_specifications_list",
            kwargs=self.kwargs,
        )

    def get_initial(self):
        return self.kwargs

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                product__slug=self.kwargs.get("slug"),
                product__department__short_name__iexact=self.kwargs["short_name"],
            )
        )


class DeleteProductSpecificationView(PermissionRequiredMixin, DeleteView):
    model = Specification
    permission_required = ("inventory.delete_specification",)
    http_method_names = ["post"]
    pk_url_kwarg = "s_pk"

    def get_success_url(self):
        self.kwargs.pop("s_pk")
        return reverse_lazy(
            "inventory:product_specifications_list",
            kwargs=self.kwargs,
        )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                product__slug=self.kwargs.get("slug"),
                product__department__short_name__iexact=self.kwargs["short_name"],
            )
        )
