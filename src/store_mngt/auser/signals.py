
from django.apps import apps
from django.contrib.admin.models import ADDITION, DELETION, CHANGE, LogEntry
from django.contrib.admin.options import get_content_type_for_model
from django.contrib.admin.utils import construct_change_message
from django.contrib.auth.models import Group as G
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from auser.models import DepartmentHead, SchoolHead, Staffmember, Storekeeper

# something is left here TODO: about staff user or is_staff
staff_user_created = Signal()
log_entry_addition = Signal()
log_entry_change = Signal()
log_entry_deletion = Signal()


def create_permission_groups(sender, plan, *args, **kwargs):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    if not Group.objects.filter(name="schoolhead").exists():
        schoolhead_group = Group.objects.create(name="schoolhead")
        schoolhead_permission = Permission.objects.filter(
            Q(codename="add_department")
            | Q(codename="view_department")
            | Q(codename="change_department")
            | Q(codename="delete_department")
            | Q(codename="deactivate_department")
            | Q(codename="activate_department")
            | Q(codename="add_departmenthead")
            | Q(codename="view_departmenthead")
            | Q(codename="change_departmenthead")
            | Q(codename="delete_departmenthead")
            | Q(codename="deactivate_departmenthead")
            | Q(codename="activate_departmenthead")

        )
        schoolhead_group.permissions.set(schoolhead_permission)

    if not Group.objects.filter(name="departmenthead").exists():
        departmenthead_group = Group.objects.create(name="departmenthead")
        departmenthead_permsission = Permission.objects.filter(
            Q(codename="add_staffmember")
            | Q(codename="view_staffmember")
            | Q(codename="delete_staffmember")
            | Q(codename="change_staffmember")
            | Q(codename="activate_staffmember")
            | Q(codename="deactivate_staffmember")
            | Q(codename="add_storeofficer")
            | Q(codename="view_storeofficer")
            | Q(codename="change_storeofficer")
            | Q(codename="delete_storeofficer")
            | Q(codename="activate_storeofficer")
            | Q(codename="deactivate_storeofficer")
            | Q(codename="add_store")
            | Q(codename="view_store")
            | Q(codename="change_store")
            | Q(codename="delete_store")
            | Q(codename="activate_store")
            | Q(codename="deactivate_store")   
        )
        departmenthead_group.permissions.set(departmenthead_permsission)

    if not Group.objects.filter(name="staffmember").exists():
        staffmember_group = Group.objects.filter(name="staffmember")
        staffmember_permission = Permission.objects.filter(
            Q(codename="borrow_item")
            | Q(codename="view_item")
            # | Q(codename="_item")
            # | Q(codename="borrow_item")
        )
        staffmember_group.permissions.set(staffmember_permission)

    if not Group.objects.filter(name="storeofficer").exists():
        storeofficer_group = Group.objects.filter(name="storeofficer")
        storeofficer_permissions = Permission.objects.filter(
            Q(codename="view_approve_item")
            | Q(codename="check_return_item")
        )

# TODO: i think i doesnt make any change
# @receiver(staff_user_created)
# def add_permission_to_staff(sender, instance=None, created=None, **kwargs):
#     user_group = G.objects.get(name="user")
#     staff_group = G.objects.get(name="staff")
#     schoolhead_group = G.objects.get(name="schoolhead")
#     departmenthead_group = G.objects.get(name="departmenthead")
    
#     instance.user.permissions.add



@receiver(post_save, sender=SchoolHead)
def add_schoolhead_group(sender, instance=None, created=None, **kwargs):
    if created:
        user_group = G.objects.get(name="user")
        schoolhead_group = G.objects.get(name="schoolhead")
        permissions = user_group.permissions.all().union(
            schoolhead_group.permissions.all()   
        )
        instance.user.permissions.all(permissions)


@receiver(post_save, sender=DepartmentHead)
def add_departmenthead_group(sender, instance=None, created=None, **kwargs):
    if created:
        user_group = G.objects.get(name="user")
        departmenthead_group = G.objects.get(name="departmenthead")
        permissions = user_group.permissions.all().union(
            departmenthead_group.permissions.all()
        )
        instance.user.permissions.all(permissions)

@receiver(post_save, sender=Staffmember)
def add_staffmember_group(sender, instance=None, created=None, **kwargs):
    if created:
        user_group =G.objects.get(name="user")
        staffmember_group = G.objects.get(name="staffmember")
        permissions = user_group.permissions.all().union(
            staffmember_group.permissions.all()
        )
        instance.user.permissions.all(permissions)


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
