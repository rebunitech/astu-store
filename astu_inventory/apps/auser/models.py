"""A list of ASTU inventory system actors model

    Date Created: 3 July, 2022
    Author: Wendirad Demelash(@wendirad)
"""
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager as SuperUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from astu_inventory.apps.auser.validators import PhoneNumberValidator


class Address(models.Model):
    """
    An abstract class which represent composite attribute 'Address'
    for sub classes.
    """

    phone_number = models.CharField(
        _("phone number"),
        max_length=13,
        unique=True,
        help_text=_("Use the format +2519********" " or 09********."),
        validators=[PhoneNumberValidator()],
    )
    location = models.CharField(
        _("address"),
        max_length=200,
        blank=True,
        null=True,
        help_text=_("Physical location."),
    )
    po_box = models.CharField(
        _("P.O Box"), max_length=10, blank=True, null=True, help_text=_("Personal P.O Box, if you have one.")
    )

    class Meta:
        abstract = True


class Department(models.Model):
    """A moodel that represents department inside the college"""

    class StatusChoices(models.IntegerChoices):
        ACTIVE = 1, _("Active")
        DEACTIVATED = 0, _("Deactivated")

    name = models.CharField(_("name"), max_length=150, help_text=_("Name of the department."))
    short_name = models.CharField(
        _("short name"), max_length=10, help_text=_("Abbrivated name of the department. eg CSE, ECE, EPCE")
    )
    description = models.TextField(
        _("description"), max_length=1000, help_text=_("Short description about the department.")
    )
    status = models.SmallIntegerField(
        _("status"),
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        help_text=_(
            "Designates that this department is active in the college."
            "Deactivating the department makes all it's decendants (staffs, stores, labs) inactive in the system"
        ),
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_name

    class Meta:
        db_table = "department"
        verbose_name = _("department")
        verbose_name_plural = _("departments")


class UserManager(SuperUserManager):
    """Custom user manager, needed because username field is changed into staff_id.

    This manager replace every use of username into staff_id.
    """

    def _create_user(self, staff_id, email, password, **extra_fields):
        """
        Create and save a user with the given staff_id, email, and password.
        """
        if not staff_id:
            raise ValueError("The given staff ID must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        staff_id = GlobalUserModel.normalize_staff_id(staff_id)
        user = self.model(staff_id=staff_id, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, staff_id, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(staff_id, email, password, **extra_fields)

    def create_superuser(self, staff_id, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(staff_id, email, password, **extra_fields)

    def get_by_natural_key(self, staff_id):
        """used to make case insensetive lookup on the staff_id field of user."""
        return self.get(**{"%s__iexact" % self.model.USERNAME_FIELD: staff_id})


class User(AbstractUser, Address):
    """User model adds additional fields to default user model.

    Replace `username` with `staff_id` since every user is identified by their staff ID
    instead of `username`.
    """

    class SexChoices(models.TextChoices):
        MALE = "M", _("MALE")
        FEMALE = "F", _("FEMALE")

    username = None
    staff_id = models.CharField(
        _("staff ID"),
        unique=True,
        max_length=15,
        help_text=_("Unique staff ID number, that the college use to identify. "),
        error_messages={
            "unique": _("A user with that staff ID already exists."),
        },
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text=_("Active email address. Use organizational email (@astu.edu.et) if you have."),
    )
    department = models.ForeignKey(
        Department,
        verbose_name=_("department"),
        related_name="staff_members",
        on_delete=models.PROTECT,
        limit_choices_to={"status": 1},
        null=True,
    )
    sex = models.CharField(_("gender"), max_length=2, choices=SexChoices.choices, blank=True, null=True)
    profile_picture = models.ImageField(_("profile picture"), upload_to="profile_pictures/", default="default.svg")

    @classmethod
    def normalize_staff_id(cls, staff_id):
        return staff_id.replace(" ", "").upper()

    objects = UserManager()

    USERNAME_FIELD = "staff_id"
    REQUIRED_FIELDS = ["email", "phone_number"]

    class Meta:
        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        """Return user staff ID and full name"""
        return "%s (%s)" % (self.get_full_name(), self.staff_id)
