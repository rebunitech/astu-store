import os

from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from auser.models import College, CollegeUser, Department


class AssignUserMixin:
    def get_user(self, user_pk, **kwargs):
        return get_object_or_404(CollegeUser, pk=user_pk, **kwargs)

    def get_college(self, short_name, **kwargs):
        return get_object_or_404(College, short_name=short_name, **kwargs)

    def get_department(self, short_name, **kwargs):
        return get_object_or_404(Department, short_name=short_name, **kwargs)

    def get_groups(self, groups):
        Q.default = Q.OR
        return Group.objects.filter(*[Q(name=name) for name in groups])


class CreateUserMixin(AssignUserMixin):
    template_name = "auser/add.html"

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "groups"):
            raise AttributeError(
                f"{self.__class__.__name__} is missing attribute groups."
            )
        if not isinstance(self.groups, (str, tuple, list, set)):
            raise TypeError(
                f"{self.__class__.__name__} groups attribue expect str, tuple, list or set. given {type(self.groups).__name__}."
            )
        super().__init__(*args, **kwargs)

    def get_new_username(self):
        return os.urandom(3).hex()

    def form_valid(self, form):
        username = self.get_new_username()
        form.instance.username = username
        self.object = form.save()
        self.object.set_password(username)
        self.object.groups.set(self.get_groups())
        return super().form_valid(form)

    def get_groups(self):
        if isinstance(self.groups, str):
            self.groups = (self.groups,)
        return super().get_groups(self.groups)


class ActiveCollegeRequiredMixin:
    pk_url_kwarg = "short_name"

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "pk_url_kwarg"):
            raise AttributeError(
                f"{self.__class__.__name__} is missing attribute pk_url_kwarg"
            )
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not College.objects.filter(
            short_name=self.kwargs[self.pk_url_kwarg], status="active"
        ).exists():
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


# class HiddenFieldMixin:


# def get_form(self, form_class=None):
#     form = super().get_form(form_class=form_class)
#     if isinstance(self.hidden_fields, str):
#         self.hidden_fields = (self.hidden_fields,)
#     for field in self.hidden_fields:
#         form[field].field.widget.attrs['disabled'] = True
#     return form
