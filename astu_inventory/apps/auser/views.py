"""ASTU Inventory auser views

Each class represents a logic layer of the project.

    Date Created: 3 July, 2022
    Author: Wendirad Demelash(@wendirad)
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView


class ProfileEditView(
    PermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    """Generic view used to update user profile"""

    model = get_user_model()
    fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "sex",
        "location",
        "po_box",
        "profile_picture",
    )
    success_url = reverse_lazy("auser:edit_profile")
    permission_required = ("auser.change_user",)
    template_name = "auser/profile_edit.html"
    success_message = _("Your profile updated successfully.")
    extra_context = {"title": _("Edit Profile")}

    def setup(self, request, *args, **kwargs):
        kwargs.update({"pk": request.user.pk})
        super().setup(request, *args, **kwargs)
