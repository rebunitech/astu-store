import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as import uuid

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



class Lab(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "ACT", _("Active")
        INACTIVE = "INA", _("Inactive")

    lab_assistant = models.ManyToManyField(
        UserModel,
        verbose_name=_("lab assistant"),
        related_name="labs",
        limit_choices_to={"is_lab_assistant": True},
    )
    department = models.ForeignKey(
        Department,
        verbose_name="department",
        related_name="labs",
        on_delete=models.CASCADE,
    )
    block = models.IntegerField(_("block"), validators=[MinValueValidator(1)])
    room = models.IntegerField(_("room"), validators=[MinValueValidator(1)])
    status = models.CharField(
        _("status"),
        max_length=3,
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
        return f"{self.department.short_name} B{self.block} R{self.room}"


class Table(models.Model):
    
    table_id = models.CharField(
        _("Table ID"), max_length=50, unique=True, default=uuid_hex
    )
    lab = models.ForeignKey(
        Lab, verbose_name="lab", related_name="tables", on_delete=models.CASCADE
    )
    remark = models.TextField(_("remark"), max_length=255, blank=True)
    is_working =  models.BooleanField(
        _("is working"),
        default=True,
        help_text=_("Is this table work properly ? | Default is True"),
    )

    class Meta:
        db_table = "table"
        verbose_name = _("table")
        verbose_name_plural = _("tables")

    def __str__(self):
        return self.table_id




class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_("Slug"))
    description = models.TextField(verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name=_("Creator"), null=True
    )

    class Meta:
        db_table = "categories"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Save slug field."""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class GeneralItem(modes.Model):

    class TypeChoises(models.TextChoices):
        CONSUMEBLE = "CONS", "Consumable"
        NONCONSUMEBLE = "NCONS", "Non-Consumeble"

    name = models.CharField(max_length=50, verbose_name=_("Name"))
    slug = models.SlugField(max_length=max_length=100, unique=True, verbose_name=_("Slug"))
    category = models.ForeignKey(
        Category,
        verbose_name=_("Category"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="generalitems",
        help_text=mark_safe(
            _(
                "Choose a category for this General ItemImg. +"
                "<a href='/store/category/add' target='_blank'>Add new category</a>"
            )
        ),
    )
    store = models.ForeignKey(
        Store, verbose_name="store", related_name="items", on_delete=models.CASCADE, null=True, blank=True
    )
    lab = models.ForeignKey(
        Lab, verbose_name="lab", related_name="items", on_delete=models.CASCADE, null=True, blank=True
    )
    remark = models.TextField(verbose_name=_("Remark"))
    itemType = models.CharField(
        _("Item Type"),
        max_length= 15,
        choices= TypeChoises.choices,
    )

    class Meta:
        db_table = "generalitems"
        verbose_name = _("general_item")
        verbose_name_plural = _("general_items")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Save slug field."""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Mesurment(models.Model):
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        db_table = "mesurment"
        verbose_name = _("mesurment")
        verbose_name_plural = _("mesurments")

    def __str__(self):
        return self.name



class BrandORType(models.Model):

    name = chained_model_field.CharField(max_length=50, verbose_name=_("Name"))
    quantity = models.IntegerField(_("Quantity"), validators=[MinValueValidator(1)])
    supplier = models.CharField(_("supplier"), max_length=255, blank=True, null=True)
    critical_no = models.IntegerField(help_text=_("Min number of Item that must be in store"))








class Item(models.Model):

    class StatusChoices(models.TextChoices):
        ACTIVE = "ACT", "Active"
        INACTIVE = "INA", "Inactive"

    

    class ForWhomChoises(models.TextChoices):
        UG = "UG", "For Under Gradguate"
        PG = "PG", "For Post Gradguate"
        BOTH = "BOTH", "For Both"

    name = models.CharField(_("name"), max_length=255, db_index=True, unique=True)
    description = models.TextField(_("description"), blank=True)
    
    quantity = models.IntegerField(_("quantity"), validators=[MinValueValidator(1)])
    dead_stock_number = models.CharField(_("dead stock number"), max_length=50)
    store = models.ForeignKey(
        Store, verbose_name="store", related_name="items", on_delete=models.CASCADE, null=True, blank=True
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
    lab = models.ForeignKey(
        Lab, verbose_name="lab", related_name="items", on_delete=models.CASCADE, null=True, blank=True
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
    year = models.IntegerField(
        _("year"), validators=[MinValueValidator(1900)], blank=True, null=True
    )
    supplier = models.CharField(_("supplier"), max_length=255, blank=True, null=True)
    exp_date = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True)
    for_whom = models.CharField(
        _("for whom"),
        max_length=20,
        choices=ForWhomChoises.choices,
        default=ForWhomChoises.BOTH,
        )
    status = models.CharField(
        _("status"),
        max_length=3,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )
    critical_no = models.IntegerField(help_text=_("Min number of Item that must be in store"))
    remark = models.TextField(_("remark"), max_length=255, blank=True)

    class Meta:
        db_table = "item"
        verbose_name = _("item")
        verbose_name_plural = _("items")

    def __str__(self):
        return self.name


class ItemImg(models.Model):
    item = models.ForeignKey(
        Item, verbose_name=_("item"), related_name="imgs", on_delete=models.CASCADE)
    img = models.ImageField(upload_to='uploads', null=True, blank=True)
    remark = models.CharField(max_length=250,)



    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")



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
