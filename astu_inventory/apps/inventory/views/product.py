from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from astu_inventory.apps.auser.models import Department
from astu_inventory.apps.core.views import ImportView
from astu_inventory.apps.inventory.forms import AddProductForm, ImportProductForm, UpdateProductForm
from astu_inventory.apps.inventory.models import Category, Measurment, Product, SubCategory


class AddProductView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = AddProductForm
    template_name = "inventory/product/add.html"
    success_url = reverse_lazy("inventory:products_list")
    permission_required = "inventory.add_product"
    success_message = _("Product '%(name)s' is successfully added!")
    extra_context = {"title": _("Add Product")}


class UpdateProductView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = UpdateProductForm
    template_name = "inventory/product/update.html"
    success_url = reverse_lazy("inventory:products_list")
    permission_required = "inventory.change_product"
    success_message = _("Product '%(name)s' is updated successfully!")
    extra_context = {"title": _("Update Product")}

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset().filter(department__short_name__iexact=self.kwargs["short_name"])
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(department=user.department)


class ListProductsView(PermissionRequiredMixin, ListView):
    model = Product
    context_object_name = "products"
    permission_required = "inventory.view_product"
    extra_context = {"title": _("Products")}
    template_name = "inventory/product/list.html"

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(Q(department=user.department))


class DeleteProductView(PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = "inventory.delete_product"
    http_method_names = ["post"]
    success_url = reverse_lazy("inventory:products_list")

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset().filter(department__short_name__iexact=self.kwargs["short_name"])
        if user.is_superuser or user.is_college_dean:
            return qs
        return qs.filter(Q(department=user.department))


class ImportProductsView(PermissionRequiredMixin, ImportView):
    model = Product
    required_fields = ["Name", "Department", "Sub Category", "Kind", "Measurement", "Critical Number"]
    db_field_name = ["name", "department", "sub_category", "kind", "measurment", "critical_no"]
    foreign_keys = {
        "department": (Department, "short_name__iexact"),
        "sub_category": (SubCategory, "name"),
        "measurment": (Measurment, "name"),
    }
    success_url = reverse_lazy("inventory:products_list")
    validation_form = ImportProductForm
    permission_required = "auser.can_import_products"
    choices_list_work_sheet_name = "Choices"

    @staticmethod
    def run_on_object(product):
        product.category = product.sub_category.category
        product.save()

    def write_choices(self, worksheet):
        department_choices = [department["short_name"] for department in Department.objects.values("short_name")]
        sub_category_choices = [sub_category["name"] for sub_category in SubCategory.objects.values("name")]
        measurment_choices = [measurment["name"] for measurment in Measurment.objects.values("name")]
        self.department_count = self.write_choice_form_list(department_choices, worksheet, 0)
        self.sub_category_count = self.write_choice_form_list(sub_category_choices, worksheet, 1)
        self.measurment_count = self.write_choice_form_list(measurment_choices, worksheet, 2)

    def add_validation(self, worksheet):
        worksheet.data_validation(
            1,
            1,
            1048575,
            1,
            {
                "validate": "list",
                "source": f"={self.choices_list_work_sheet_name}!$A$1:$A${self.department_count}",
                "input_title": "Select a department",
                "input_message": "Please select department from a given list only.",
                "error_title": "Invalid department selected.",
                "error_message": "Please select department from a given list only.",
            },
        )
        worksheet.data_validation(
            1,
            2,
            1048575,
            2,
            {
                "validate": "list",
                "source": f"={self.choices_list_work_sheet_name}!$B$1:$B${self.sub_category_count}",
                "input_title": "Select a sub category",
                "input_message": "Please select sub category from a given list only.",
                "error_title": "Invalid sub category selected",
                "error_message": "Please select sub category from a given list only.",
            },
        )
        worksheet.data_validation(
            1,
            3,
            1048575,
            3,
            {
                "validate": "list",
                "source": ["CONSUMABLE", "NON_CONSUMABLE"],
                "input_title": "Select a kind",
                "input_message": "Please select kind from a given list only.",
                "error_title": "Invalid kind selected",
                "error_message": "Please select kind from a given list only.",
            },
        )
        worksheet.data_validation(
            1,
            4,
            1048575,
            4,
            {
                "validate": "list",
                "source": f"={self.choices_list_work_sheet_name}!$C$1:$C${self.sub_category_count}",
                "input_title": "Select a measurment",
                "input_message": "Please select measurment from a given list only.",
                "error_title": "Invalid measurment selected",
                "error_message": "Please select measurment from a given list only.",
            },
        )
        worksheet.data_validation(
            1,
            6,
            1048575,
            6,
            {
                "validate": "integer",
                "criteria": ">",
                "value": -1,
                "input_title": "Enter critical number for this product",
                "input_message": "Please enter critical number greater than or equals to 0.",
                "error_title": "Invalid critical number",
                "error_message": "Critical number must be greater than or equals to 0.",
            },
        )
