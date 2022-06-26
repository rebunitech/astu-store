from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

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
    bio = models.TextField(
        _("Bio"), help_text=_("Tell us about your self"), null=True, blank=True
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
    REQUIRED_FIELDS = ["email", "phone_number", "sex"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "user"
        indexes = [
            models.Index(fields=["id"], name="user_id_idx"),
            models.Index(fields=["username"], name="user_username_idx"),
        ]

    @property
    def is_school_representative(self):
        return hasattr(self, "schoolrepresentative")

    @property
    def is_department_representative(self):
        return hasattr(self, "departmentrepresentative")


class SchoolOrDepartment(models.Model):
    """Abstruct model that used in school and departments."""

    name = models.CharField(_("name"), max_length=150)
    short_name = models.CharField(_("short name"), max_length=10)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.short_name


class School(SchoolOrDepartment):
    class Meta:
        verbose_name = _("school")
        verbose_name_plural = _("schools")
        db_table = "school"


class Department(SchoolOrDepartment):
    school = models.ForeignKey(
        School,
        verbose_name=_("school"),
        related_name="departments",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("department")
        verbose_name_plural = _("departments")
        db_table = "department"


class SchoolRepresentative(User):
    school = models.ForeignKey(
        School,
        verbose_name=_("school"),
        related_name="school_representatives",
        on_delete=models.CASCADE,
    )


class DepartmentRepresentative(User):
    department = models.ForeignKey(
        Department,
        verbose_name=_("department"),
        related_name="department_representatives",
        on_delete=models.CASCADE,
    )


class StoreKeeper(User):
    department = models.ForeignKey(
        Department,
        verbose_name=_("department"),
        related_name="store_keepers",
        on_delete=models.CASCADE,
    )


class Staff(User):
    department = models.ForeignKey(
        Department,
        verbose_name=_("department"),
        related_name="staffs",
        on_delete=models.CASCADE,
    )
