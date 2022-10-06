from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from astu_inventory.apps.core.views import ImportView
from astu_inventory.apps.inventory.forms import ItemForm
from astu_inventory.apps.inventory.models import Item, Product


class AddItemView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = "inventory/item/add.html"
    success_url = reverse_lazy("inventory:items_list")
    permission_required = "inventory.add_item"
    success_message = _("Item is successfully added!")
    extra_context = {"title": _("Add Item")}

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.product.availables += self.object.quantity
        self.object.product.save()
        return response

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        user = self.request.user
        if user.is_superuser or user.is_college_dean:
            return form
        form["product"].field.queryset = form["product"].field.queryset.filter(department=user.department)
        return form


class ListItemsView(PermissionRequiredMixin, ListView):
    model = Item
    context_object_name = "items"
    permission_required = "inventory.view_item"
    extra_context = {"title": _("Items")}
    template_name = "inventory/item/list.html"
    paginated_by = 50

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset().select_related("product", "product__measurment")
        if user.is_superuser or user.is_college_dean:
            return qs
        if user.is_department_head:
            return qs.filter(Q(store__department=user.department))
        return qs.filter(Q(store__store_officers__pk=user.pk))


class UpdateItemView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = "inventory/item/update.html"
    success_url = reverse_lazy("inventory:items_list")
    permission_required = "inventory.change_item"
    success_message = _("Item is updated successfully!")
    extra_context = {"title": _("Update Item")}

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.has_changed() and "quantity" in form.changed_data:
            difference = form.instance.quantity - form.initial.get("quantity")
            self.object.product.availables += difference
            self.object.product.save()
        return response

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.is_college_dean:
            return qs
        if user.is_department_head:
            return qs.filter(Q(store__department=user.department))
        return qs.filter(Q(store__store_officers__pk=user.pk))


class DeleteItemView(PermissionRequiredMixin, DeleteView):
    model = Item
    permission_required = "inventory.delete_item"
    http_method_names = ["post"]
    success_url = reverse_lazy("inventory:items_list")

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.is_college_dean:
            return qs
        if user.is_department_head:
            return qs.filter(Q(store__department=user.department))
        return qs.filter(Q(store__store_officers__pk=user.pk))


class ImportItemsView(PermissionRequiredMixin, ImportView):
    model = Item
    required_fields = ("Product", "Dead Stock Number", "Quantity")
    db_field_name = ("product", "dead_stock_number", "quantity")
    success_url = reverse_lazy("inventory:items_list")
    permission_required = "auser.can_import_items"
    choices_list_work_sheet_name = "Choices"

    def get_product(self, data):
        name, department = data.split(" | ")
        return Product.objects.get(name=name, department__short_name__iexact=department)

    def get_foreign_keys(self):
        return {"product": self.get_product}

    def add_validation(self, worksheet):
        worksheet.data_validation(
            1,
            0,
            1048575,
            0,
            {
                "validate": "list",
                "source": f"={self.choices_list_work_sheet_name}!$A$1:$A${self.product_count}",
                "input_title": "Select a department",
                "input_message": "Please select department from a given list only.",
                "error_title": "Invalid department selected.",
                "error_message": "Please select department from a given list only.",
            },
        )

    def _write_product_choice(self, worksheet):
        product_choices = [
            "%s | %s" % (product["name"], product["department__short_name"][:5])
            for product in Product.objects.values("name", "department__short_name")
        ]
        self.product_count = 0
        for ix, choice in enumerate(product_choices):
            self.product_count += 1
            worksheet.write(ix, 0, choice)

    def write_choices(self, worksheet):
        self._write_product_choice(worksheet)
