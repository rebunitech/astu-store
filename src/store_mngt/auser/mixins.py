"""gradient_infosys auser custom mixins
	
    Created by: Wendirad Demelash
    Last modified by: Wendirad Demelash
"""
from django.contrib.auth.mixins import LoginRequiredMixin

from auser.signals import (log_entry_adition, log_entry_change,
                           log_entry_deletion)


class CurrentUserMixin:
    """A Mixin that automatically add user pk to kwargs, to prevent sending user id over url."""

    pk_kwargs = "pk"

    def setup(self, request, *args, **kwargs):
        kwargs.update({self.pk_kwargs: request.user.pk})
        return super().setup(request, *args, **kwargs)


class SuperuserRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class LogEntryAdditionMixin:
    """Save changes related to object"""

    def get_success_url(self):
        """Save log entry when form is valid"""
        log_entry_adition.send(
            sender=self.model,
            instance=self.object,
            user_id=self.request.user.id,
            created=True,
        )
        return super().get_success_url()


class LogEntryChangeMixin:
    """Save changes related to object"""

    def form_valid(self, form):
        """Save log entry when form is valid"""
        log_entry_change.send(
            sender=self.model,
            instance=self.object,
            form=form,
            user_id=self.request.user.id,
            is_adition=False,
        )
        return super().form_valid(form)


class LogEntryDeletionMixin:
    """Create log entity related to object"""

    def form_valid(self, form):
        """Save log entry when form is valid"""
        log_entry_deletion.send(
            sender=self.model, instance=self.object, user_id=self.request.user.id
        )
        return super().form_valid(form)
