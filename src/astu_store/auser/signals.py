from django.apps import apps
from django.db.models import Q


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
