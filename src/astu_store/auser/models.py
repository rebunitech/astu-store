from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey

from auser.validators import PhoneNumberValidator


class Address(models.Model):
    """
    An abstract class which represent composite attribute 'Address'
    for sub classes.
    """

    email = models.EmailField(
        _("email"),
        unique=True,
    )
    phone_number = models.CharField(
        _("phone number"),
        max_length=13,
        unique=True,
        validators=[PhoneNumberValidator()],
    )
    location = models.CharField(
        _("address"),
        max_length=200,
        blank=True,
        null=True,
        help_text=_("Physical location."),
    )
    po_box = models.CharField(_("P.O Box"), max_length=10, blank=True, null=True)

    class Meta:
        abstract = True


class AbstractUser(models.Model):
    """Abstract model need to user for both user and instructors"""

    class SexChoices(models.TextChoices):
        MALE = "M", _("MALE")
        FEMALE = "F", _("FEMALE")

    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    sex = models.CharField(
        _("Gender"), max_length=2, choices=SexChoices.choices, blank=True, null=True
    )
    profile_picture = models.ImageField(
        _("Profile picture"), upload_to="profile_pictures/", default="default.svg"
    )
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()


class User(AbstractUser, AbstractBaseUser, PermissionsMixin, Address):
    """Custom user model used as primary user in the platform."""

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting account"
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = [
        "email",
        "phone_number",
    ]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "user"
        indexes = [
            models.Index(fields=["id"], name="user_id_idx"),
            models.Index(fields=["username"], name="user_username_idx"),
        ]
        permissions = [
            ("can_add_college_representative", "Can add college representative"),
            ("can_view_college_representative", "Can change college representative"),
            ("can_change_college_representative", "Can view college representative"),
            ("can_delete_college_representative", "Can delete college representative"),
            (
                "can_activate_college_representative",
                "Can activate college representative",
            ),
            (
                "can_deactivate_college_representative",
                "Can deactivate college representative",
            ),
            ("can_add_department_representative", "Can add department representative"),
            (
                "can_view_department_representative",
                "Can change department representative",
            ),
            (
                "can_change_department_representative",
                "Can view department representative",
            ),
            (
                "can_delete_department_representative",
                "Can delete department representative",
            ),
            (
                "can_activate_department_representative",
                "Can activate department representative",
            ),
            (
                "can_deactivate_department_representative",
                "Can deactivate department representative",
            ),
            ("can_add_staff_member", "Can add staff member"),
            ("can_view_staff_member", "Can change staff member"),
            ("can_change_staff_member", "Can view staff member"),
            ("can_delete_staff_member", "Can delete staff member"),
            ("can_activate_staff_member", "Can activate staff member"),
            ("can_deactivate_staff_member", "Can deactivate staff member"),
            ("can_add_store_keeper", "Can add store keeper"),
            ("can_view_store_keeper", "Can change store keeper"),
            ("can_change_store_keeper", "Can view store keeper"),
            ("can_delete_store_keeper", "Can delete store keeper"),
            ("can_activate_store_keeper", "Can activate store keeper"),
            ("can_deactivate_store_keeper", "Can deactivate store keeper"),
        ]

    @property
    def is_college_representative(self):
        if self.is_superuser:
            return True
        return self.groups.filter(name="college_representative").exists()

    @property
    def is_department_representative(self):
        if self.is_superuser:
            return True
        return self.groups.filter(name="department_representative").exists()

    @property
    def is_store_keeper(self):
        if self.is_superuser:
            return True
        return self.groups.filter(name="store_keeper").exists()

    @property
    def is_staff_member(self):
        if self.is_superuser:
            return True
        return self.groups.filter(name="staff_member").exists()


class CollegeOrDepartment(models.Model):
    """Abstruct model that used in college and departments."""

    class StatusChoices(models.TextChoices):
        ACTIVE = "active", _("Active")
        DEACTIVATED = "deactivated", _("Deactivated")

    name = models.CharField(_("name"), max_length=150)
    short_name = models.CharField(_("short name"), unique=True, max_length=10)
    description = models.TextField(_("description"))
    status = models.CharField(
        _("status"),
        max_length=15,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.short_name

    def normalize_short_name(self, short_name):
        return short_name.upper().replace(" ", "")

    def save(self, *args, **kwargs):
        self.short_name = self.normalize_short_name(self.short_name)
        return super().save(*args, **kwargs)


class College(CollegeOrDepartment):
    class Meta:
        verbose_name = _("college")
        verbose_name_plural = _("colleges")
        db_table = "college"


class Department(CollegeOrDepartment):
    college = models.ForeignKey(
        College,
        verbose_name=_("college"),
        related_name="departments",
        on_delete=models.CASCADE,
        limit_choices_to={"status": "active"},
    )

    class Meta:
        verbose_name = _("department")
        verbose_name_plural = _("departments")
        db_table = "department"


class CollegeUser(User):
    college = models.ForeignKey(
        College,
        verbose_name=_("college"),
        related_name="users",
        limit_choices_to={"status": "active"},
        on_delete=models.CASCADE,
    )
    department = ChainedForeignKey(
        Department,
        chained_field="college",
        chained_model_field="college",
        verbose_name="department",
        related_name="staffs",
        limit_choices_to={"status": "active"},
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = _("college_user")
        verbose_name = _("in college user")
        verbose_name_plural = _("in college users")
