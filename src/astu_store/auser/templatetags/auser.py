import imp
from ast import arg

from django import template
from django.contrib.admin.options import get_content_type_for_model
from django.urls import reverse_lazy

register = template.Library()


@register.filter(name="ctype")
def ctype(view):
    return get_content_type_for_model(view.model).pk


@register.filter(name="reverse")
def reverse(url, args=None):
    return reverse_lazy(url, args=[args])
