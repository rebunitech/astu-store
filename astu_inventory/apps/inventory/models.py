"""ASTU Inventory inventory models

Each class represents a single form.

    Date Created: 9 July, 2022
    Author: Ashebir wondemeneh(@Ashebir07)
"""


import os

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey

from astu_inventory.apps.auser.models import Department

UserModel = get_user_model()


def get_ID():
    return os.urandom(4).hex()


class Store(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "ACTIVE", _("Active")
        INACTIVE = "INACTIVE", _("Inactive")

    store_officers = models.ManyToManyField(
        UserModel,
        verbose_name=_("store officers"),
        related_name="store_offcers",
    )
    department = models.ForeignKey(
        Department,
        verbose_name="department",
        related_name="stores",
        on_delete=models.PROTECT,
    )
    block = models.IntegerField(_("block"), validators=[MinValueValidator(1)])
    room = models.IntegerField(_("room"), validators=[MinValueValidator(1)])
    status = models.CharField(
        _("status"),
        max_length=8,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        help_text=_("Is the store on use?"),
    )
    remark = models.TextField(_("remark"), max_length=255, blank=True)

    class Meta:
        db_table = "store"
        verbose_name = _("store")
        verbose_name_plural = _("stores")
        unique_together = (("block", "room"),)

    def __str__(self):
        return f"{self.department.short_name} Store B{self.block} R{self.room}"


class Shelf(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    shelf_id = models.CharField(
        _("shelf ID"), max_length=50, unique=True, default=get_ID
    )
    store = models.ForeignKey(
        Store, verbose_name="store", related_name="shelves", on_delete=models.CASCADE
    )
    no_row = models.IntegerField(
        _("Number of row(s)"), validators=[MinValueValidator(1)]
    )
    no_column = models.IntegerField(
        _("Number of column(s)"), validators=[MinValueValidator(1)]
    )
    status = models.CharField(
        _("status"),
        max_length=8,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )
    remark = models.TextField(_("remark"), max_length=255, blank=True)

    class Meta:
        db_table = "shelf"
        verbose_name = _("shelf")
        verbose_name_plural = _("shelves")

    def __str__(self):
        return self.shelf_id


class Lab(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "ACTIVE", _("Active")
        INACTIVE = "INACTIVE", _("Inactive")

    lab_assistant = models.ManyToManyField(
        UserModel,
        verbose_name=_("lab assistant"),
        related_name="labs",
    )
    department = models.ForeignKey(
        Department,
        verbose_name="department",
        related_name="labs",
        on_delete=models.PROTECT,
    )
    block = models.IntegerField(_("block"), validators=[MinValueValidator(1)])
    room = models.IntegerField(_("room"), validators=[MinValueValidator(1)])
    status = models.CharField(
        _("status"),
        max_length=8,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        help_text=_("Is the lab on work?"),
    )
    remark = models.TextField(_("remark"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("lab")
        verbose_name_plural = _("labs")
        unique_together = ("block", "room")

    def __str__(self):
        return f"{self.department.short_name} Lab B{self.block} R{self.room}"


class Table(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "ACTIVE", _("Active")
        INACTIVE = "INACTIVE", _("Inactive")

    table_id = models.CharField(
        _("table ID"), max_length=50, unique=True, default=get_ID
    )
    lab = models.ForeignKey(
        Lab, verbose_name="lab", related_name="tables", on_delete=models.CASCADE
    )
    status = models.CharField(
        _("status"),
        max_length=8,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )
    remark = models.TextField(_("remark"), max_length=255, blank=True)

    class Meta:
        db_table = "table"
        verbose_name = _("table")
        verbose_name_plural = _("tables")

    def __str__(self):
        return self.table_id


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_("slug"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        db_table = "categories"
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Save slug field."""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("name"))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_("slug"))
    category = models.ForeignKey(
        Category,
        verbose_name=_("category"),
        on_delete=models.PROTECT,
        null=True,
        related_name="sub_categories",
    )
    remark = models.TextField(verbose_name=_("remark"))

    class Meta:
        db_table = "sub_category"
        verbose_name = _("sub category")
        verbose_name_plural = _("sub categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Save slug field."""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Measurment(models.Model):
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        db_table = "measurement"
        verbose_name = _("measurement")
        verbose_name_plural = _("measurements")

    def __str__(self):
        return self.name


class Product(models.Model):
    class KindChoices(models.TextChoices):
        CONSUMABLE = "CONSUMABLE", _("Consumable")
        NON_CONSUMABLE = "NON_CONSUMABLE", _("Non-Consumable")

    name = models.CharField(max_length=50, verbose_name=_("name"))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_("slug"))
    category = models.ForeignKey(
        Category, verbose_name=_("category"), on_delete=models.PROTECT
    )
    sub_category = ChainedForeignKey(
        SubCategory,
        chained_field="category",
        chained_model_field="category",
        verbose_name="sub category",
        related_name="products",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.PROTECT,
    )
    # college = models.ForeignKey(
    #     College, verbose_name=_("college"), on_delete=models.PROTECT
    # )
    department = ChainedForeignKey(
        Department,
        chained_field="college",
        chained_model_field="college",
        verbose_name="department",
        related_name="products",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.PROTECT,
    )
    kind = models.CharField(
        max_length=25, verbose_name=_("kind"), choices=KindChoices.choices
    )
    measurment = models.ForeignKey(
        Measurment, verbose_name=_("measurement"), on_delete=models.PROTECT
    )
    critical_no = models.IntegerField(
        help_text=_("min number of Item that must be in store")
    )

    class Meta:
        db_table = "product"
        verbose_name = _("product")
        verbose_name_plural = _("products")

    @property
    def is_under_critical(self):
        return self.availables < self.critical_no

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Save slug field."""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def availables(self):
        total_item = self.items.aggregate(total_item=Coalesce(Sum("quantity"), 0))[
            "total_item"
        ]
        total_borrow_request = self.borrow_requests.aggregate(
            total_borrow_request=Coalesce(Sum("quantity", filter=Q(status=1) | Q(status=6)), 0)
        )["total_borrow_request"]
        return total_item - total_borrow_request


class Item(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    class PurposeChoices(models.TextChoices):
        UG = "UG", _("Undergraduate")
        PG = (
            "PG",
            _("Postgraduate"),
        )
        BOTH = "BOTH", _("Undergraduate and Postgraduate")

    name = models.CharField(_("name"), max_length=255, db_index=True)
    description = models.TextField(_("description"), blank=True)
    quantity = models.IntegerField(_("quantity"), validators=[MinValueValidator(1)])
    dead_stock_number = models.CharField(_("dead stock number"), max_length=50)
    purpose = models.CharField(
        _("purpose"),
        max_length=10,
        choices=PurposeChoices.choices,
        default=PurposeChoices.BOTH,
    )
    store = models.ForeignKey(
        Store,
        verbose_name="store",
        related_name="stores",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    shelf = ChainedForeignKey(
        Shelf,
        chained_field="store",
        chained_model_field="store",
        verbose_name="shelf",
        related_name="shelves",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    lab = models.ForeignKey(
        Lab,
        verbose_name="lab",
        related_name="items",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    table = ChainedForeignKey(
        Table,
        chained_field="lab",
        chained_model_field="lab",
        verbose_name="table",
        related_name="items",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    expiration_date = models.DateField(_("expiration date"), blank=True)
    year_of_purchase = models.IntegerField(
        _("year of purchase"),
        validators=[MinValueValidator(1900)],
        blank=True,
        null=True,
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        related_name="items",
        on_delete=models.PROTECT,
    )
    supplier = models.CharField(_("supplier"), max_length=255, blank=True, null=True)
    status = models.CharField(
        _("status"),
        max_length=8,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )
    remark = models.TextField(_("remark"), max_length=255, blank=True)

    class Meta:
        db_table = "item"
        verbose_name = _("item")
        verbose_name_plural = _("items")

    def __str__(self):
        return self.name


class SpecificationType(models.Model):
    name = models.CharField(_("name"), max_length=255)
    si_unit = models.CharField(
        _("SI unit"), max_length=255, help_text=_("e.g. m, kg, etc.")
    )

    class Meta:
        db_table = "specification_types"
        verbose_name = _("specification type")
        verbose_name_plural = _("specification types")

    def __str__(self):
        return f"{self.name} ({self.si_unit})"


class Specification(models.Model):
    item = models.ForeignKey(
        Item,
        verbose_name="item",
        related_name="specifications",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    product = models.ForeignKey(
        Product,
        verbose_name="product",
        related_name="specifications_product",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text=_("Product eg. Hp,Dell,Toshiba, if you have one.")
    )
    specification_type = models.ForeignKey(
        SpecificationType,
        verbose_name="specification type",
        related_name="specifications_types",
        on_delete=models.PROTECT,
    )
    value = models.CharField(_("value"), max_length=255)
    remark = models.TextField(_("remark"), max_length=255, blank=True)

    class Meta:
        db_table = "specifications"
        verbose_name = _("specification")
        verbose_name_plural = _("specifications")
        unique_together = (
            ("item", "specification_type"),
            ("product", "specification_type"),
        )
