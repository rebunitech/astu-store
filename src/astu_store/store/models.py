import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from auser.models import Department


class Store(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "ACT", "Active"
        INACTIVE = "INA", "Inactive"

    department = models.ForeignKey(
        Department,
        verbose_name="department",
        related_name="stores",
        on_delete=models.CASCADE,
    )
    block = models.IntegerField(_("block"), validators=[MinValueValidator(1)])
    room = models.IntegerField(_("number"), validators=[MinValueValidator(1)])
    status = models.CharField(
        _("status"),
        max_length=3,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        help_text=_("Is the store on use?"),
    )
    remark = models.CharField(_("remark"), max_length=255, blank=True)

    class Meta:
        db_table = "store"
        verbose_name = _("store")
        verbose_name_plural = _("stores")
        unique_together = ("block", "room")

    def __str__(self):
        return f"{self.department.short_name}-{self.block}-{self.room}"


class Shelf(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "ACT", "Active"
        INACTIVE = "INA", "Inactive"

    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(
        Store, verbose_name="store", related_name="shelves", on_delete=models.CASCADE
    )
    no_row = models.IntegerField(_("row"), validators=[MinValueValidator(1)])
    no_column = models.IntegerField(_("column"), validators=[MinValueValidator(1)])
    status = models.CharField(
        _("status"),
        max_length=3,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )
    remark = models.CharField(_("remark"), max_length=255, blank=True)

    class Meta:
        db_table = "shelf"
        verbose_name = _("shelf")
        verbose_name_plural = _("shelves")

    def __str__(self):
        return f"{self.store.block}-{self.store.room}-{self.no_row}-{self.no_column} [{self.id.hex}]"


class Item(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "ACT", "Active"
        INACTIVE = "INA", "Inactive"

    name = models.CharField(_("name"), max_length=255, db_index=True)
    description = models.TextField(_("description"), blank=True)
    quantity = models.IntegerField(_("quantity"), validators=[MinValueValidator(1)])
    dead_stock_number = models.IntegerField(
        _("dead stock number"), validators=[MinValueValidator(1)]
    )
    shelf = models.ForeignKey(
        Shelf,
        verbose_name="shelf",
        related_name="items",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    store = models.ForeignKey(
        Store, verbose_name="store", related_name="items", on_delete=models.CASCADE
    )
    year = models.IntegerField(_("year"), validators=[MinValueValidator(1)])
    supplier = models.CharField(_("supplier"), max_length=255)
    status = models.CharField(
        _("status"),
        max_length=3,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )
    remark = models.CharField(_("remark"), max_length=255, blank=True)

    class Meta:
        db_table = "item"
        verbose_name = _("item")
        verbose_name_plural = _("items")


class SpecificationType(models.Model):
    name = models.CharField(_("name"), max_length=255)
    si_unit = models.CharField(
        _("SI unit"), max_length=255, help_text=_("e.g. m, kg, etc.")
    )

    class Meta:
        db_table = "specification_type"
        verbose_name = _("specification type")
        verbose_name_plural = _("specification types")


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
    value = models.FloatField(_("value"))
    remark = models.CharField(_("remark"), max_length=255, blank=True)

    class Meta:
        db_table = "specification"
        verbose_name = _("specification")
        verbose_name_plural = _("specifications")
        unique_together = ("item", "specification_type")
