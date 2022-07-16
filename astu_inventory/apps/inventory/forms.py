from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from astu_inventory.apps.inventory.models import (
    Category,
    Item,
    Product,
    ProductImage,
    Shelf,
    Specification,
    SubCategory,
    Table,
)


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


class AddProductForm(forms.ModelForm):
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

    def clean(self):
        cleaned_data = super().clean()
        slug = slugify(cleaned_data.get("name"))
        department = cleaned_data.get("department")
        if Product.objects.filter(slug=slug, department=department).exists():
            raise ValidationError(f"This product exists in {department} department.")
        return cleaned_data


class ImportProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "department", "sub_category", "kind", "measurment", "critical_no")

    def clean(self):
        cleaned_data = super().clean()
        slug = slugify(cleaned_data.get("name"))
        department = cleaned_data.get("department")
        if Product.objects.filter(slug=slug, department=department).exists():
            raise ValidationError(f"This product exists in {department} department.")
        self.instance.category = cleaned_data.get("sub_category").category
        return cleaned_data


class UpdateProductForm(forms.ModelForm):
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

    def clean(self):
        cleaned_data = super().clean()
        slug = slugify(cleaned_data.get("name"))
        department = cleaned_data.get("department")
        instance = self.instance
        if Product.objects.exclude(pk=instance.pk).filter(slug=slug, department=department).exists():
            raise ValidationError(f"This product exists in {department} department.")
        return cleaned_data


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            "product",
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
        if not ((store and shelf) or (lab and table)):
            raise ValidationError("You must select either store and shelf or lab and table.")
        if (store or shelf) and (lab or table):
            raise ValidationError("You can't choose store and lab together. Please choose only one of them.")
        return cleaned_data


class AddProductSpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = ("specification_type", "value", "remark")

    def clean(self):
        cleaned_data = super().clean()
        specification_type = cleaned_data.get("specification_type")
        department_short_name = self.initial.get("short_name")
        product_slug = self.initial.get("slug")
        product = get_object_or_404(Product, slug=product_slug, department__short_name__iexact=department_short_name)
        if Specification.objects.filter(product=product, specification_type=specification_type).exists():
            raise ValidationError(
                "This specification exists for this product. Please add other specification or update existing one."
            )
        self.instance.product = product
        return cleaned_data


class UpdateProductSpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = ("specification_type", "value", "remark")

    def clean(self):
        cleaned_data = super().clean()
        specification_type = cleaned_data.get("specification_type")
        department_short_name = self.initial.get("short_name")
        product_slug = self.initial.get("slug")
        product = get_object_or_404(Product, slug=product_slug, department__short_name__iexact=department_short_name)
        if (
            Specification.objects.exclude(pk=self.instance.pk)
            .filter(product=product, specification_type=specification_type)
            .exists()
        ):
            raise ValidationError(
                "This specification exists for this product. Please add other specification or update existing one."
            )
        return cleaned_data


class AddItemSpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = ("specification_type", "value", "remark")

    def clean(self):
        cleaned_data = super().clean()
        specification_type = cleaned_data.get("specification_type")
        item_pk = self.initial.get("pk")
        item = get_object_or_404(Item, pk=item_pk)
        if Specification.objects.filter(item=item, specification_type=specification_type).exists():
            raise ValidationError(
                "This specification exists for this item. Please add other specification or update existing one."
            )
        self.instance.item = item
        return cleaned_data


class UpdateItemSpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = ("specification_type", "value", "remark")

    def clean(self):
        cleaned_data = super().clean()
        specification_type = cleaned_data.get("specification_type")
        item_pk = self.initial.get("pk")
        item = get_object_or_404(Item, pk=item_pk)
        if (
            Specification.objects.exclude(pk=self.instance.pk)
            .filter(item=item, specification_type=specification_type)
            .exists()
        ):
            raise ValidationError(
                "This specification exists for this item. Please add other specification or update existing one."
            )
        return cleaned_data


class AddProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ("image",)

    def clean(self):
        cleaned_data = super().clean()
        department_short_name = self.initial.get("short_name")
        product_slug = self.initial.get("slug")
        product = get_object_or_404(Product, slug=product_slug, department__short_name__iexact=department_short_name)
        self.instance.product = product
        return cleaned_data
