from django import template

register = template.Library()

from astu_inventory.apps.help.models import Help


@register.inclusion_tag("help/help.html")
def get_help(app_name, view_name, user_has_perm=False):
    help_ = Help.objects.filter(app_name=app_name, view_name=view_name)
    if help_:
        help_ = help_.first()
    return {"help": help_, "user_has_perm": user_has_perm}
