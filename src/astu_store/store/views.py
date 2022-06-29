from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from store.models import Item, Shelf, Specification, SpecificationType, Store


class AddSpecificationTypeView(
    PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    model = SpecificationType
    fields = (
        "name",
        "si_unit",
    )
    permission_required = ("store.add_specificationtype",)
    success_message = _('Specification type "%(name)s" added successfully.')
    template_name = "store/specification/type/add.html"
    success_url = reverse_lazy("store:list_specification_types")
    extra_context = {"title": _("Add specification type")}


class ListSpecificationTypesView(PermissionRequiredMixin, ListView):
    model = SpecificationType
    permission_required = ("store.view_specificationtype",)
    context_object_name = "specification_types"
    template_name = "store/specification/type/list.html"
    extra_context = {"title": _("Specification Types")}


class UpdateSpecificationTypeView(
    PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = SpecificationType
    fields = ("name", "si_unit")
    permission_required = ("store.change_specificationtype",)
    success_message = _('Specification type "%(name)s" updated successfully.')
    template_name = "store/specification/type/update.html"
    success_url = reverse_lazy("store:list_specification_types")
    extra_context = {"title": _("Update specification type")}


class DeleteSpecificationTypeView(PermissionRequiredMixin, DeleteView):
    model = SpecificationType
    permission_required = ("store.delete_specificationtype",)
    success_url = reverse_lazy("store:list_specification_types")
    http_method_names = ["post"]


class AddStoreView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Store
    fields = ("department", "block", "room", "remark")
    permission_required = ("store.add_store",)
    success_message = _("Store added successfully.")
    template_name = "store/add.html"
    success_url = reverse_lazy("store:list_stores")
    extra_context = {"title": _("Add store")}


class ListStoresView(PermissionRequiredMixin, ListView):
    model = Store
    permission_required = ("store.view_store",)
    context_object_name = "stores"
    template_name = "store/list.html"
    extra_context = {"title": _("Stores")}


class UpdateStoreView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Store
    fields = ("department", "block", "room", "status", "remark")
    permission_required = ("store.change_store",)
    success_message = _("Store updated successfully.")
    template_name = "store/update.html"
    success_url = reverse_lazy("store:list_stores")
    extra_context = {"title": _("Update store")}


class DeleteStoreView(PermissionRequiredMixin, DeleteView):
    model = Store
    permission_required = ("store.delete_store",)
    success_url = reverse_lazy("store:list_stores")
    http_method_names = ["post"]


class AddShelfView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Shelf
    fields = ("shelf_id", "no_row", "no_column", "remark")
    permission_required = ("store.add_shelf",)
    success_message = _("Shelf added successfully.")
    template_name = "store/shelf/add.html"
    extra_context = {"title": _("Add shelf")}
    pk_url_kwarg = "store_pk"

    def get_store(self):
        return get_object_or_404(Store, pk=self.kwargs.get("store_pk"))

    def form_valid(self, form):
        form.instance.store = self.get_store()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "store:list_shelves", kwargs={"store_pk": self.kwargs.get("store_pk")}
        )


class ListShelvesView(PermissionRequiredMixin, ListView):
    model = Shelf
    permission_required = ("store.view_shelf",)
    context_object_name = "shelves"
    template_name = "store/shelf/list.html"
    extra_context = {"title": _("Shelves")}

    def get_queryset(self):
        return super().get_queryset().filter(store__pk=self.kwargs.get("store_pk"))


class UpdateShelfView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Shelf
    fields = ("shelf_id", "no_row", "no_column", "status", "remark")
    permission_required = ("store.change_shelf",)
    success_message = _("Shelf updated successfully.")
    template_name = "store/shelf/update.html"
    extra_context = {"title": _("Update shelf")}
    pk_url_kwarg = "uuid"

    def get_success_url(self):
        return reverse_lazy(
            "store:list_shelves", kwargs={"store_pk": self.get_object().store.pk}
        )


class DeleteShelfView(PermissionRequiredMixin, DeleteView):
    model = Shelf
    permission_required = ("store.delete_shelf",)
    success_url = reverse_lazy("store:list_shelves")
    pk_url_kwarg = "uuid"
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy(
            "store:list_shelves", kwargs={"store_pk": self.get_object().store.pk}
        )


class AddItemView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Item
    fields = (
        "name",
        "description",
        "store",
        "shelf",
        "dead_stock_number",
        "quantity",
        "year",
        "supplier",
        "remark",
    )
    permission_required = ("store.add_item",)
    success_message = _('Item "%(name)s" added successfully.')
    template_name = "store/item/add.html"
    # success_url = reverse_lazy("store:list_items")
    extra_context = {"title": _("Add item")}

    def get_success_url(self):
        print(self.object)
        return reverse_lazy(
            "store:add_specification", kwargs={"item_pk": self.object.pk}
        )


class ListItemsView(PermissionRequiredMixin, ListView):
    model = Item
    permission_required = ("store.view_item",)
    context_object_name = "items"
    template_name = "store/item/list.html"
    extra_context = {"title": _("Items")}

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return qs
        elif user.is_college_representative():
            return qs.filter(store__department__college=user.college)
        return qs.filter(store__department=user.department)


class UpdateItemView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    fields = (
        "name",
        "description",
        "store",
        "shelf",
        "dead_stock_number",
        "quantity",
        "year",
        "supplier",
        "remark",
    )
    permission_required = ("store.change_item",)
    success_message = _('Item "%(name)s" updated successfully.')
    success_url = reverse_lazy("store:list_items")
    template_name = "store/item/update.html"
    extra_context = {"title": _("Update item")}


class DeleteItemView(PermissionRequiredMixin, DeleteView):
    model = Item
    permission_required = ("store.delete_item",)
    success_url = reverse_lazy("store:list_items")
    http_method_names = ["post"]


class AddSpecificationView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Specification
    fields = ("specification_type", "value", "remark")
    permission_required = ("store.add_specification",)
    success_message = _("Specification added successfully.")
    template_name = "store/specification/add.html"
    extra_context = {"title": _("Add specification")}
    pk_url_kwarg = "item_pk"

    def get_item(self):
        return get_object_or_404(Item, pk=self.kwargs.get("item_pk"))

    def form_valid(self, form):
        form.instance.item = self.get_item()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "store:list_specifications",
            kwargs={"item_pk": self.kwargs.get("item_pk")},
        )


class ListSpecificationsView(PermissionRequiredMixin, ListView):
    model = Specification
    permission_required = ("store.view_specification",)
    context_object_name = "specifications"
    template_name = "store/specification/list.html"
    extra_context = {"title": _("Specifications")}

    def get_queryset(self):
        return super().get_queryset().filter(item__pk=self.kwargs.get("item_pk"))


class UpdateSpecificationView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Specification
    fields = ("specification_type", "value", "remark")
    permission_required = ("store.change_specification",)
    success_message = _("Specification updated successfully.")
    template_name = "store/item/update.html"
    extra_context = {"title": _("Update item")}

    def get_success_url(self):
        return reverse_lazy(
            "store:list_specifications",
            kwargs={"item_pk": self.get_object().item.pk},
        )


class DeleteSpecificationView(PermissionRequiredMixin, DeleteView):
    model = Specification
    permission_required = ("store.delete_specification",)
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy(
            "store:list_specifications",
            kwargs={"item_pk": self.get_object().item.pk},
        )
