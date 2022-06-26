

from django.apps import apps
from django.contrib.admin.models import ADDITION, DELETION, CHANGE, LogEntry
from django.contrib.admin.options import get_content_type_for_model
from django.contrib.admin.utils import construct_change_message
from django.contrib.auth.models import Group as G
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal



log_entry_addition = Signal()

@receiver(log_entry_addition)
def save_addition_log_entry(sender, instance=None, user_id=None, created=None, **kwargs):
    if created:
        LogEntry.objects.log_action(
            user_id=user_id,
            content_type_id=get_content_type_for_model(instance).pk,
            object_id=instance.pk,
            object_repr=str(instance),
            action_flag=ADDITION,
            change_message=[{"added": {}}],
        )

