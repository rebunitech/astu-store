"""A list of ASTU inventory auth signals.

Each signals represent an event in the system

    Date Created: 4 July, 2022
    Author: Wendirad Demelash(@wendirad)
"""

from django.apps import apps


def create_roles(sender, plan, *args, **kwargs):
    """Create roles of system actors. One or more roles will be assigned for one user.
    The role determines the permissions of the user.

    Roles:
        College Dean: Representative of college, and responsible for managing departments.
        Department Head: Representative of single department, and responsible for managing staff memmbers.
        Store Officer: Representative of department stores, and responsible for borrowing items from store.
        Lab Assistant: Representative of department labs, and responsible for managing lab items.
        Staff Member: Represents a signle member of one department, and have permission to borrow items.

    NB: The signal is connected to post_migration signal when the app is ready.
    """
    ROLES = [
        'college dean',
        'department head',
        'store officer',
        'lab assistant',
        'staff member'
    ]

    Group = apps.get_model('auth', 'Group')
    for role in ROLES:
        Group.objects.get_or_create(name=role)
