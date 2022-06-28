from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from inventory.models import Category, Product, Shelf, SubCategory, Table


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

    def clean_name(self):
        name = self.cleaned_data["name"]
        if Category.objects.filter(slug=slugify(name)).exists():
            raise ValidationError("Category with this name aleady exists.")
        return name


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = (
            "category",
            "name",
        )

    def clean_name(self):
        name = self.cleaned_data["name"]
        if SubCategory.objects.filter(slug=slugify(name)).exists():
            raise ValidationError("Sub category with this name aleady exists.")
        return name


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "category", "sub_category", "kind", "critical_no")

    def clean_name(self):
        name = self.cleaned_data["name"]
        if Product.objects.filter(slug=slugify(name)).exists():
            raise ValidationError("Product with this name aleady exists.")
        return name
