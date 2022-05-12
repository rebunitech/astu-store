from django.db import models

# Create your models here.
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _


# class Item(models.Model):
#     name = models.CharField(max_length=100, verbose_name=_("Name"))
#     itemId = models.CharField(_("item id"), max_length=200)
#     quantity = models.IntegerField(unique=True)
#     dsn = models.CharField(_("DSN"), max_length=200)
    




