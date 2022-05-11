from django.contrib import messages
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, RedirectView, UpdateView

from auser.forms import ChangePermissionForm, UserChangeForm
from auser.mixins import CurrentUserMixin, LogEntryChangeMixin

UserModel = get_user_model()


class ProfileEditView(
    PermissionRequiredMixin,
    CurrentUserMixin,
    SuccessMessageMixin,
    LogEntryChangeMixin,
    UpdateView,
):
    """Generic view used to update user profile"""

    model = UserModel
    form_class = UserChangeForm
    success_url = reverse_lazy("auser:profile_edit")
    permission_required = ("auser.change_user",)
    template_name = "auser/user/profile_edit.html"
    success_message = _("%(first_name)s %(last_name)s profile updated successfully")
    extra_context = {"title": _("Edit Profile")}


class ChangePermissionView(
    PermissionRequiredMixin, SuccessMessageMixin, LogEntryChangeMixin, UpdateView
):
    """Generic view used to change user permission"""

    model = UserModel
    form_class = ChangePermissionForm
    permission_required = ("auser.change_user_permissions",)
    success_message = _("%(first_name)s %(last_name)s permission changed successfully")
    template_name = "auser/user/change_permission.html"
    extra_context = {"title": _("Change User Permission")}

    def form_valid(self, form):
        form.cleaned_data.update(
            {"first_name": self.object.first_name, "last_name": self.object.last_name}
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("auser:change_permission", kwargs={"pk": self.object.pk})


class PasswordResetDoneView(SuccessMessageMixin, RedirectView):
    """Redirect view for password reset done"""

    permanent = False
    success_message = _(
        "We’ve emailed you instructions for setting your password, if an account "
        "exists with the email you entered. You should receive them shortly.\n\n"
        "If you don’t receive an email, please make sure you’ve entered the address "
        "you registered with, and check your spam folder."
    )
    url = reverse_lazy("auser:login")

    def get_redirect_url(self, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().get_redirect_url(*args, **kwargs)


class UserActionsListView(PermissionRequiredMixin, ListView):
    model = LogEntry
    template_name = "auser/user/user_actions_list.html"
    context_object_name = "user_actions"
    permission_required = ("admin.view_logentry",)
    extra_context = {"title": _("User Actions")}

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.kwargs["pk"])
