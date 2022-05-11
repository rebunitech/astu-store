from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.flatpages.models import FlatPage


class FlatPageForm(forms.ModelForm):
    class Meta:
        model = FlatPage
        fields = ("url", "title", "content", "registration_required")
        widgets = {
            "registration_required": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "content": CKEditorWidget(),
        }

