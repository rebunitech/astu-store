"""ASTU Inventory inventory views

Each class represents a single form.

    Date Created: 9 July, 2022
    Author: Ashebir wondemeneh(@Ashebir07)
"""



from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from astu_inventory.apps.inventory.models import Category, Item, Product, Shelf, SubCategory, Table
from django.contrib.auth import get_user_model
UserModel = get_user_model()
class ShelfForm(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = ("shelf_id", "no_row", "no_column", "status", "remark")

    def clean_shelf_id(self):
        shelf_id = self.cleaned_data["shelf_id"]
        return slugify(shelf_id)


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ("table_id", "status", "remark")

    def clean_table_id(self):
        table_id = self.cleaned_data["table_id"]
        return slugify(table_id)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = (
            "category",
            "name",
        )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "name",
            "department",
            "category",
            "sub_category",
            "kind",
            "measurment",
            "critical_no",
        )

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            "product",
            "name",
            "dead_stock_number",
            "quantity",
            "purpose",
            "store",
            "shelf",
            "lab",
            "table",
            "expiration_date",
            "year_of_purchase",
            "supplier",
            "status",
            "remark",
        )

    def clean(self):
        cleaned_data = super().clean()
        store = cleaned_data.get("store")
        lab = cleaned_data.get("lab")
        shelf = cleaned_data.get("shelf")
        table = cleaned_data.get("table")

        if (store or shelf) and (lab or table):
            raise ValidationError(
                "You cann't choose store and lab together. Please choose only one of them."
            )
        return cleaned_data
