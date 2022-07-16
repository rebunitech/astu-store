# flake8: noqa
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "astu_inventory.apps.core"

    def ready(self):
        from astu_inventory.apps.core import signals  # NOQA
