from django.apps import apps
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.admin.options import get_content_type_for_model
from django.contrib.admin.utils import construct_change_message
from django.contrib.auth.models import Group as G
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

from auser.models import DepartmentHead, Student

staff_user_created = Signal()
log_entry_adition = Signal()
log_entry_change = Signal()
log_entry_deletion = Signal()


def create_permission_groups(sender, plan, *args, **kwargs):
    Group = apps.get_model("auth", "Group")
    if plan and not Group.objects.filter(name="user").exists():
        Permission = apps.get_model("auth", "Permission")
        user_group = Group.objects.create(name="user")
        user_permissions = Permission.objects.filter(
            Q(codename="view_user")
            | Q(codename="change_user")
            | Q(codename="like_post")
        )
        user_group.permissions.set(user_permissions)

    if plan and not Group.objects.filter(name="staff").exists():
        staff_group = Group.objects.create(name="staff")
        staff_permissions = Permission.objects.filter(
            Q(codename="add_departmentHead")
            | Q(codename="activate_department_head")
            | Q(codename="deactivate_department_head")
            | Q(codename="change_departmentHead")
            | Q(codename="view_departmentHead")
            | Q(codename="delete_departmentHead")
            | Q(codename="view_student")
            | Q(codename="change_student")
            | Q(codename="deactivate_student")
            | Q(codename="activate_student")
            | Q(codename="delete_student")
            | Q(codename="add_service")
            | Q(codename="change_service")
            | Q(codename="view_service")
            | Q(codename="delete_service")
        )
        staff_group.permissions.set(staff_permissions)

    if plan and not Group.objects.filter(name="department_head").exists():
        content_creator_group = Group.objects.create(name="department_head")
        content_creator_permissions = Permission.objects.filter(
            Q(codename="add_post")
            | Q(codename="change_post")
            | Q(codename="view_post")
            | Q(codename="delete_blog")
            | Q(codename="add_category")
            | Q(codename="change_category")
            | Q(codename="view_category")
            | Q(codename="delete_category")
            | Q(codename="add_tag")
            | Q(codename="change_tag")
            | Q(codename="view_tag")
            | Q(codename="delete_tag")
        )

    if plan and not Group.objects.filter(name="student").exists():
        student_group = Group.objects.create(name="student")
        student_permissions = Permission.objects.filter(**{})


@receiver(staff_user_created)
def add_permissions_to_staff(sender, instance=None, created=None, **kwargs):
    if created:
        user_group = G.objects.get(name="user")
        staff_group = G.objects.get(name="staff")
        content_creator_group = G.objects.get(name="content_creator")
        permissions = (
            user_group.permissions.all()
            .union(staff_group.permissions.all())
            .union(content_creator_group.permissions.all())
        )
        instance.user_permissions.set(permissions)


@receiver(post_save, sender=DepartmentHead)
def add_content_creator_group(sender, instance=None, created=None, **kwargs):
    if created:
        user_group = G.objects.get(name="user")
        content_creator_group = G.objects.get(name="department_head")
        permissions = user_group.permissions.all().union(
            content_creator_group.permissions.all()
        )
        instance.user_permissions.set(permissions)


@receiver(post_save, sender=Student)
def add_student_group(sender, instance=None, created=None, **kwargs):
    if created:
        user_group = G.objects.get(name="user")
        student_group = G.objects.get(name="student")
        permissions = user_group.permissions.all().union(
            student_group.permissions.all()
        )
        instance.user_permissions.set(permissions)


@receiver(log_entry_adition)
def save_addtion_log_entry(sender, instance=None, user_id=None, created=None, **kwargs):
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
