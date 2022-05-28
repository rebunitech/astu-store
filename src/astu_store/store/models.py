import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey

from auser.models import Department

UserModel = get_user_model()


class Store(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "ACT", _("Active")
        INACTIVE = "INA", _("Inactive")

    store_keepers = models.ManyToManyField(
        UserModel,
        verbose_name=_("store keeper"),
        related_name="stores",
        limit_choices_to={"is_store_keeper": True},
    )
    department = models.ForeignKey(
        Department,
        verbose_name="department",
        related_name="stores",
        on_delete=models.CASCADE,
    )
    block = models.IntegerField(_("block"), validators=[MinValueValidator(1)])
    room = models.IntegerField(_("room"), validators=[MinValueValidator(1)])
    status = models.CharField(
        _("status"),
        max_length=3,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        help_text=_("Is the store on use?"),
    )
    remark = models.TextField(_("remark"), max_length=255, blank=True)

    class Meta:
        db_table = "store"
        verbose_name = _("store")
        verbose_name_plural = _("stores")
        unique_together = ("block", "room")

    def __str__(self):
        return f"{self.department.short_name} B{self.block} R{self.room}"


def uuid_hex():
    return uuid.uuid4().hex


class Shelf(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "ACT", "Active"
        INACTIVE = "INA", "Inactive"

    shelf_id = models.CharField(
        _("shelf ID"), max_length=50, unique=True, default=uuid_hex
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
        max_length=3,
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


class Item(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "ACT", "Active"
        INACTIVE = "INA", "Inactive"

    name = models.CharField(_("name"), max_length=255, db_index=True)
    description = models.TextField(_("description"), blank=True)
    quantity = models.IntegerField(_("quantity"), validators=[MinValueValidator(1)])
    dead_stock_number = models.CharField(_("dead stock number"), max_length=50)
    store = models.ForeignKey(
        Store, verbose_name="store", related_name="items", on_delete=models.CASCADE
    )
    shelf = ChainedForeignKey(
        Shelf,
        chained_field="store",
        chained_model_field="store",
        verbose_name="shelf",
        related_name="items",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    year = models.IntegerField(
        _("year"), validators=[MinValueValidator(1900)], blank=True, null=True
    )
    supplier = models.CharField(_("supplier"), max_length=255, blank=True, null=True)
    status = models.CharField(
        _("status"),
        max_length=3,
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
        db_table = "specification_type"
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
    )
    specification_type = models.ForeignKey(
        SpecificationType,
        verbose_name="specification type",
        related_name="specifications",
        on_delete=models.CASCADE,
    )
    value = models.CharField(_("value"), max_length=255)
    remark = models.TextField(_("remark"), max_length=255, blank=True)

    class Meta:
        db_table = "specification"
        verbose_name = _("specification")
        verbose_name_plural = _("specifications")
        unique_together = ("item", "specification_type")
