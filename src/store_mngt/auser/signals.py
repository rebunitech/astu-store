from django.apps import apps
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.admin.options import get_content_type_for_model
from django.contrib.admin.utils import construct_change_message
from django.contrib.auth.models import Group as G
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

from auser.models import DepartmentHead, Staffmember

school_head_created = Signal()
log_entry_adition = Signal()
log_entry_change = Signal()
log_entry_deletion = Signal()


def create_permission_groups(sender, plan, *args, **kwargs):
    Group = apps.get_model("auth", "Group")
    if plan and not Group.objects.filter(name="user").exists(): # TODO: check wende
        Permission = apps.get_model("auth", "Permission")
        staffmember_group = Group.objects.create(name="user")
        staffmember_permissions = Permission.objects.filter(
            Q(codename="view_user")
            | Q(codename="change_user")
        )
        staffmember_group.permissions.set(staffmember_permissions)

    if plan and not Group.objects.filter(name="schoolHead").exists():
        schoolHead_group = Group.objects.create(name="schoolHead")
        schoolHead_permissions = Permission.objects.filter(
            Q(codename="add_department_head")  # TODO: department == contentCreator
            | Q(codename="activate_department_head")
            | Q(codename="deactivate_department_head")
            | Q(codename="change_department_head")
            | Q(codename="view_department_head")
            | Q(codename="delete_department_head")
            | Q(codename="add_store_keeper")
            | Q(codename="change_store_keeper")
            | Q(codename="view_store_keeper")
            | Q(codename="activate_store_keeper")
            | Q(codename="deactivate_store_keeper")
            | Q(codename="delete_store_keeper")
            | Q(codename="add_store")
            | Q(codename="change_store")
            | Q(codename="view_store")
            | Q(codename="activate_store")
            | Q(codename="deactivate_store")
            | Q(codename="delete_store")
            | Q(codename="view_staffmember") 
            | Q(codename="change_staffmember")
            | Q(codename="deactivate_staffmember")
            | Q(codename="activate_staffmember")
            | Q(codename="delete_staffmember")
            | Q(codename="add_staffmember")
        )
        schoolHead_group.permissions.set(schoolHead_permissions)

    if plan and not Group.objects.filter(name="department_head").exists():
        department_head_group = Group.objects.create(name="department_head")
        department_head_permissions = Permission.objects.filter(
            Q(codename="add_store_keeper")
            | Q(codename="change_store_keeper")
            | Q(codename="view_store_keeper")
            | Q(codename="activate_store_keeper")
            | Q(codename="deactivate_store_keeper")
            | Q(codename="delete_store_keeper")
            | Q(codename="add_store")
            | Q(codename="change_store")
            | Q(codename="view_store")
            | Q(codename="activate_store")
            | Q(codename="deactivate_store")
            | Q(codename="delete_store")
            | Q(codename="view_staffmember") 
            | Q(codename="change_staffmember")
            | Q(codename="deactivate_staffmember")
            | Q(codename="activate_staffmember")
            | Q(codename="delete_staffmember")
            | Q(codename="add_staffmember")
        )

# TODO: what is the difference between user and student in former GIS proj....wende???
    if plan and not Group.objects.filter(name="staffmember").exists():
        staffmember_group = Group.objects.create(name="staffmember")
        staffmember_permissions = Permission.objects.filter(**{})


@receiver(school_head_created)
def add_permissions_to_school_head(sender, instance=None, created=None, **kwargs):
    if created:
        user_group = G.objects.get(name="user")
        school_head_group = G.objects.get(name="school_head")
        department_head_group = G.objects.get(name="department_head")
        permissions = (
            user_group.permissions.all()
            .union(school_head_group.permissions.all())
            .union(department_head_group.permissions.all())
        )
        instance.user_permissions.set(permissions)


@receiver(post_save, sender=DepartmentHead)
def add_department_head_group(sender, instance=None, created=None, **kwargs):
    if created:
        user_group = G.objects.get(name="user") # TODO: check name=user
        department_head_group = G.objects.get(name="department_head")
        permissions = user_group.permissions.all().union(
            department_head_group.permissions.all()
        )
        instance.user_permissions.set(permissions)


@receiver(post_save, sender=Staffmember)
def add_staffmember_group(sender, instance=None, created=None, **kwargs):
    if created:
        user_group = G.objects.get(name="user")
        staffmember_group = G.objects.get(name="staffmember")
        permissions = user_group.permissions.all().union(
            staffmember_group.permissions.all()
        )
        instance.user_permissions.set(permissions)


@receiver(log_entry_adition)
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


@receiver(log_entry_change)
def save_change_log_entry(sender, instance=None, form=None, user_id=None, **kwargs):
    if form.has_changed():
        message = construct_change_message(form, None, False)
        LogEntry.objects.log_action(
            user_id=user_id,
            content_type_id=get_content_type_for_model(instance).pk,
            object_id=instance.pk,
            object_repr=str(instance),
            action_flag=CHANGE,
            change_message=message,
        )


@receiver(log_entry_deletion)
def save_deletion_log_entry(sender, instance=None, user_id=None, **kwargs):
    LogEntry.objects.log_action(
        user_id=user_id,
        content_type_id=get_content_type_for_model(instance).pk,
        object_id=instance.pk,
        object_repr=str(instance),
        action_flag=DELETION,
    )
