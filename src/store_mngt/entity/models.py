from django.db import models
import datetime
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from entity.validator import PhoneNumberValidator




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



class School(models.Model):
    name = models.CharField(_("name"), max_length=100)
    shortName = models.CharField(max_length=100)


# class SchoolRepresentative(models.Model):
#     name = models.CharField(_("name"), max_length=100)



class Department(models.Model):
    name = models.CharField(_("name"), max_length=100)


