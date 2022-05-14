
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
    

class User(Address):
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
    is_schoolHead = models.BooleanField(
        _("schoolHead status"),
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


class DepartmentHead(User):
    """ Department head are users mainly responsible for approve item requist, add item, add store and others"""

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

    class Meta:
        verbose_name = _("store keeper")
        verbose_name_plural = _("store keepers")
        db_table = "store_keeper"
        permissions = [
            ("can_deactivate_store_keeper", "Can deactivate store keeper"),
            ("can_activate_store_keeper", "Can activate store keeper"),
        ]


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
    school_of_dept = models.ForeignKey(School,
                                        on_delete=models.SET_NULL,
                                        verbose_name=_("dpartment belongs to school"),
                                        null=True)

    