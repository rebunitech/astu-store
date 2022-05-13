
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
    

class User(models.Model):
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
            ("can_view_staff", "Can view staff"),
            ("can_change_staff", "Can change staff"),
            ("can_add_staff", "Can add staff"),
            ("can_delete_staff", "Can delete staff"),
            ("can_change_user_permissions", "Can change user permissions"),
        ]


class SchoolHead(User):
    """ School head are users responsible for managing items belong school and others"""
    class Meta:
        verbose_name = _("content creator")
        verbose_name_plural = _("content creators")
        db_table = "content_creator"
        permissions = [
            ("can_deactivate_content_creator", "Can deactivate content creator"),
            ("can_activate_content_creator", "Can activate content creator"),
        ]

class DepartmentHead(User):
    """ Department head are users mainly responsible for approve item requist, add item, add store and others"""

    class Meta:
        verbose_name = _("content creator")
        verbose_name_plural = _("content creators")
        db_table = "content_creator"
        permissions = [
            ("can_deactivate_content_creator", "Can deactivate content creator"),
            ("can_activate_content_creator", "Can activate content creator"),
        ]


class Staffmember(User):
    """ Staffmember are requesting items users. """

    class Meta:
        verbose_name = _("staff member")
        verbose_name_plural = _("staffmembers")
        db_table = "staffmember"
        permissions = [
            ("can_deactivate_staffmember", "Can deactivate staff member"),
            ("can_activate_staffmember", "Can activate staff member"),
        ]


  