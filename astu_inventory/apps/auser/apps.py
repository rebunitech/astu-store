"""ASTU Inventory auser app Configuration

Each class represents a single configuration for auser app.

    Date Created: 4 July, 2022
    Author: Wendirad Demelash(@wendirad)
"""

from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AuserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "astu_inventory.apps.auser"

    def ready(self):
        """Create roles if not exists after migration occurs"""

        from astu_inventory.apps.auser.signals import create_roles

        post_migrate.connect(create_roles, sender=self)
