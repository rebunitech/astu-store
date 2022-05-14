from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auser'

    def ready(self):
        from auser.signals import create_permission_groups

        post_migrate.connect(create_permission_groups, sender=self)
