from django import forms
from django_summernote.widgets import SummernoteWidget
from astu_inventory.apps.help.models import Help


def get_app_name_choices():
    return (
        ("auser", "auser"),
        ("core", "core"),
        ("inventory", "inventory"),
    )

def get_view_name_choices():
    return (

    )

class HelpForm(forms.ModelForm):
    app_name = forms.ChoiceField(choices=get_app_name_choices())
    view_name = forms.ChoiceField(choices=get_view_name_choices())
    class Meta:
        model = Help
        fields = (
            "app_name",
            "view_name",
            "content",
        )
        widgets = {
            'content': SummernoteWidget()
        }
