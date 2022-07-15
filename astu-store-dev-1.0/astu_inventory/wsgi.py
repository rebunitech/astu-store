"""
WSGI config for astu_inventory project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from decouple import config

environment = config("ASTU_INVENTORY_ENVIRONMENT", default="production")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"astu_inventory.settings.{environment}")

application = get_wsgi_application()
