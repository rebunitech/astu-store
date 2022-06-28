from tokenize import Single
from django.apps import apps
from django.db.models import Q

from django.contrib.admin.models import ADDITION, DELETION, CHANGE, LogEntry
from django.dispatch import Signal, receiver
from django.contrib.admin.options import get_content_type_for_model
from django.contrib.admin.utils import construct_change_message

log_entry_addition = Signal()
log_entry_change = Signal()
log_entry_deletion = Signal()

def create_permission_groups(sender, plan, *args, **kwargs):
    """
    Create groups when a signal is send. the signal is connected when app is ready
    and send signal after creating migrations on the app.
    """
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    if plan:
        if not Group.objects.filter(name="college_representative").exists():
            college_representative_group = Group.objects.create(
                name="college_representative"
            )
            college_representative_permissions = Permission.objects.filter(
                Q(codename="view_college")
                | Q(codename="view_college_representative")
                | Q(codename="add_department")
                | Q(codename="view_department")
                | Q(codename="change_department")
                | Q(codename="delete_department")
                | Q(codename="change_college_representative")
                | Q(codename="add_department_representative")
                | Q(codename="view_department_representative")
                | Q(codename="change_department_representative")
                | Q(codename="delete_department_representative")
                | Q(codename="activate_department_representative")
                | Q(codename="delete_department_representative")
                | Q(codename="can_change_college_representative")
            )
            college_representative_group.permissions.set(
                college_representative_permissions
            )

        if not Group.objects.filter(name="department_representative").exists():
            department_representative_group = Group.objects.create(
                name="department_representative"
            )
            department_representative_permissions = Permission.objects.filter(
                Q(codename="view_department")
                | Q(codename="view_department_representative")
                | Q(codename="change_department_representative")
                | Q(codename="add_staff_member")
                | Q(codename="view_staff_member")
                | Q(codename="change_staff_member")
                | Q(codename="delete_staff_member")
                | Q(codename="add_store_officer")
                | Q(codename="view_store_officer")
                | Q(codename="change_store_officer")
                | Q(codename="delete_store_officer")
                | Q(codename="add_store")
                | Q(codename="view_store")
                | Q(codename="change_store")
                | Q(codename="delete_store")
                | Q(codename="view_maintenancerequest")
                | Q(codename="can_decline")
                | Q(codename="view_list_declined_maintenance_request")
                | Q(codename="can_repaire")
                | Q(codename="view_list_repaired_maintenance_request")
                | Q(codename="add_failurityreport")
                | Q(codename="view_failurityreport")
                | Q(codename="add_damagereport")
                | Q(codename="add_damagereport")
                | Q(codename="can_damagemaintenancerequest")
                | Q(codename="")
                | Q(codename="")
            )
            department_representative_group.permissions.set(
                department_representative_permissions
            )

        if not Group.objects.filter(name="store_officer").exists():
            store_officer_group = Group.objects.create(name="store_officer")
            store_officer_permissions = Permission.objects.filter(
                Q(codename="view_store")
                | Q(codename="add_shelf")
                | Q(codename="view_shelf")
                | Q(codename="change_shelf")
                | Q(codename="delete_shelf")
                | Q(codename="add_item")
                | Q(codename="view_item")
                | Q(codename="change_item")
                | Q(codename="delete_item")
                | Q(codename="add_specification_type")
                | Q(codename="view_specification_type")
                | Q(codename="change_specification_type")
                | Q(codename="delete_specification_type")
                | Q(codename="add_specification")
                | Q(codename="view_specification")
                | Q(codename="change_specification")
                | Q(codename="delete_specification")
                | Q(codename="view_maintenancerequest")
                | Q(codename="add_maintenancerequest")
                | Q(codename="change_maintenancerequest")
                | Q(codename="cancel_maintenancerequest")
                | Q(codename="view_canceled_maintenancerequest")
                | Q(codename="view_list_approved_maintenance_request")
                | Q(codename="view_list_declined_maintenance_request")
                | Q(codename="can_repaire")
                | Q(codename="view_list_repaired_maintenance_request")
                | Q(codename="add_failurityreport")
                | Q(codename="view_failurityreport")
                | Q(codename="add_damagereport")
                | Q(codename="view_damagereport")
                | Q(codename="can_damagemaintenancerequest")
                | Q(codename="view_damagedmaintenacerequest")
                | Q(codename="")
            )
            store_officer_group.permissions.set(store_officer_permissions)

        if not Group.objects.filter(name="lab_assistant").exists():
            lab_assistant_group = Group.objects.create(name="lab_assistant")
            lab_assistant_permissions = Permission.objects.filter(
                Q(codename="view_store")
                | Q(codename="add_shelf")
                | Q(codename="view_shelf")
                | Q(codename="change_shelf")
                | Q(codename="delete_shelf")
                | Q(codename="add_item")
                | Q(codename="view_item")
                | Q(codename="change_item")
                | Q(codename="delete_item")
                | Q(codename="add_specification_type")
                | Q(codename="view_specification_type")
                | Q(codename="change_specification_type")
                | Q(codename="delete_specification_type")
                | Q(codename="add_specification")
                | Q(codename="view_specification")
                | Q(codename="change_specification")
                | Q(codename="delete_specification")
            )
            lab_assistant_group.permissions.set(lab_assistant_permissions)

        if not Group.objects.filter(name="staff_member").exists():
            staff_member_group = Group.objects.create(name="staff_member")
            staff_member_permissions = Permission.objects.filter(
                Q(codename="view_store")
                | Q(codename="add_shelf")
                | Q(codename="view_shelf")
                | Q(codename="change_shelf")
                | Q(codename="delete_shelf")
                | Q(codename="add_item")
                | Q(codename="view_item")
                | Q(codename="change_item")
                | Q(codename="delete_item")
                | Q(codename="add_specification_type")
                | Q(codename="view_specification_type")
                | Q(codename="change_specification_type")
                | Q(codename="delete_specification_type")
                | Q(codename="add_specification")
                | Q(codename="view_specification")
                | Q(codename="change_specification")
                | Q(codename="delete_specification")
            )
            staff_member_group.permissions.set(staff_member_permissions)


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
