import os

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView

from auser.models import CollegeUser


class CreateUserMixin(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = CollegeUser
    fields = (
        "college",
        "department",
        "email",
        "sex",
        "phone_number",
    )

    template_name = "auser/add.html"
    user_object_name = None
    extra_context = {}
    groups = None

    def check_missing_attributes_error(self, attributes):
        for attr in attributes:
            if not hasattr(self, attr):
                raise AttributeError(
                    f"{self.__class__.__name__} is missing attribute {attr}"
                )

    def __init__(self, *args, **kwargs):
        self.check_missing_attributes_error(["user_object_name", "groups"])
        self.extra_context.update({"title": f"Add {self.user_object_name}"})
        self.success_message = "User %(email)s was created successfully"

    def get_groups(self):
        return [Group(name=group_name) for group_name in self.groups]

    def get_new_username(self):
        return os.urandom(3).hex()

    def form_valid(self, form):
        user = form.save(commit=False)
        username = self.get_new_username()
        user.username = username
        user.set_password(username)
        user.save()
        user.groups.set(self.get_groups())
        return super().form_valid(form)
