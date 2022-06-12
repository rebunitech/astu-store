
from django.db import models

import datetime
from ckeditor.fields import RichTextField
from django.contrib.auth.models import (
                                         AbstractBaseUser, UserManager,
                                         PermissionsMixin
                                        )
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from auser.validator import PhoneNumberValidator


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
        blank = True,
        null = True,
        help_text=_("Physical location")
    )
    po_box = models.CharField(
        _("P.O Box"),
        max_length=10,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
    

class AbstractUser(models.Model):
    """Abstract model need to user for both user and instructors"""

    class SexChoices(models.TextChoices):
        MALE = "M", _("MALE")
        FEMALE = "F", _("FEMALE")

    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    sex = models.CharField(_("Gender"), max_length=2, choices=SexChoices.choices)
    bio = RichTextField(
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
class School(Address, models.Model):
    """ School contains some departments. """
    name = models.CharField( _("name"),
                            max_length=200,
                            null= False,
                            unique=True
                        
    )
    abbr_name = models.CharField(_("abbribation name"),
                                 max_length = 50,
                                 unique=True,
                                 null = False

    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Designates whether this school is active or not")
    )

    def __str__(self) -> str:
        return self.name

    

class Department(Address ,models.Model):
    """ Department .... """
    name = models.CharField(_("name"),
                            max_length=200,
                            null = False,
                            unique=True)

    abbr_name = models.CharField(_("abbribation name"),
                                    max_length = 50,
                                    unique=True,
                                    null = False)
    school = models.ForeignKey(School,
                                on_delete=models.CASCADE,
                                verbose_name=_("school"),
                                related_name='departments',
                                help_text=_("Select school"),
                               )
    is_active = models.BooleanField(
        _("is active"),
        default=True,
        help_text=_("Designates whether this department is active or not"),
    )

    def __str__(self) -> str:
        return self.abbr_name
    
class User(AbstractUser, AbstractBaseUser, PermissionsMixin, Address):
    """ Custom user model used as primary user in the platform. """

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

        permissions = [  
            ("can_deactivate_user", "Can deactivate user"),
            ("can_activate_user", "Can activate user"),
            ("can_view_schoolHead", "Can view schoolHead"),
            ("can_change_schoolHead", "Can change schoolHead"),
            ("can_add_schoolHead", "Can add schoolHead"),
            ("can_delete_schoolHead", "Can delete schoolHead"),
            ("can_change_user_permissions", "Can change user permissions"),
        ]


class SchoolHead(User):
    """ School head are users responsible for managing school and department activities. """

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="school_heads",
        verbose_name="school",
    )

    class Meta:
        verbose_name = _("school head")
        verbose_name_plural = _("school heads")
        db_table = "school_head"
        permissions = [
            ("can_deactivate_school_head", "Can deactivate school head"),
            ("can_activate_school_head", "Can activate school head"),
        ]

    def __str__(self):
        return self.name
class DepartmentHead(User):
    """ Department head are users mainly responsible for approve item requist, add item, add store and others"""

    department = models.ForeignKey(
                            Department,
                            on_delete=models.CASCADE,
                            related_name="departmentheads",
                            verbose_name="department",
                            
                            )
    class Meta:
        verbose_name = _("department head")
        verbose_name_plural = _("department heads")
        db_table = "department_head"
        permissions = [
            ("can_deactivate_department_head", "Can deactivate department head"),
            ("can_activate_department_head", "Can activate department head"),
        ]


class Staffmember(User):
    """ Staffmember are requesting items users. """

    department = models.ForeignKey(
                            Department,
                            on_delete=models.CASCADE,
                            related_name="staffmembers",
                            verbose_name="department",
                            
                            )

    class Meta:
        verbose_name = _("staff member")
        verbose_name_plural = _("staff members")
        db_table = "staffmember"
        permissions = [
            ("can_deactivate_staffmember", "Can deactivate staff member"),
            ("can_activate_staffmember", "Can activate staff member"),
        ]


class Storekeeper(User):
    """ Store keeper are users responsible for store that belong to them and request for meintanance item. """

    department = models.ForeignKey(
                            Department,
                            on_delete=models.CASCADE,
                            related_name="store_keepers",
                            verbose_name="department",
    )
    class Meta:
        verbose_name = _("store keeper")
        verbose_name_plural = _("store keepers")
        db_table = "store_keeper"
        permissions = [
            ("can_deactivate_store_keeper", "Can deactivate store keeper"),
            ("can_activate_store_keeper", "Can activate store keeper"),
        ]
