# from django.contrib.admin.models import LogEntry
# from django.contrib.auth.mixins import PermissionRequiredMixin
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.messages.views import SuccessMessageMixin
# from django.urls import reverse_lazy
# from django.utils.translation import gettext_lazy as _
# from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
#                                   UpdateView)

# from auser.forms import EducationBackgroundForm, ExperienceForm
# from auser.mixins import (LogEntryAdditionMixin, LogEntryChangeMixin,
#                           LogEntryDeletionMixin)
# from auser.models import (EducationBackground, Experience, Instructor,
#                           InstructorSocialMediaLink, SocialMedia)


# class InstructorListAdminView(PermissionRequiredMixin, ListView):
#     model = Instructor
#     template_name = "auser/instructor/instructor_list.html"
#     context_object_name = "instructors"
#     extra_context = {"title": _("Instructors")}
#     permission_required = ("auser.view_instructor", "auser.add_instructor")

#     def get_context_data(self, **kwargs):
#         kwargs.update(
#             {
#                 "social_medias": SocialMedia.objects.all(),
#             }
#         )
#         return super().get_context_data(**kwargs)


# class InstructorDetailAdminView(PermissionRequiredMixin, DetailView):
#     model = Instructor
#     template_name = "auser/instructor/instructor_detail.html"
#     context_object_name = "instructor"
#     permission_required = ("auser.view_instructor", "auser.add_instructor")
#     extra_context = {"title": _("Instructor")}

#     def get_content_type(self):
#         """Return content type for LogEntry"""

#         return ContentType.objects.get_for_model(self.model).pk

#     def get_object_hisotry(self):
#         """Return log entries for the object"""

#         return LogEntry.objects.filter(
#             content_type_id=self.get_content_type(), object_id=self.object.pk
#         )

#     def get_context_data(self, **kwargs):
#         kwargs.update(
#             {
#                 "object_history": self.get_object_hisotry(),
#             }
#         )
#         return super().get_context_data(**kwargs)


# class AddInstructorView(
#     PermissionRequiredMixin, SuccessMessageMixin, LogEntryAdditionMixin, CreateView
# ):
#     model = Instructor
#     template_name = "auser/instructor/instructor_add.html"
#     fields = ("first_name", "last_name", "email", "phone_number", "sex")
#     extra_context = {"title": _("Add Instructor")}
#     permission_required = ("auser.add_instructor",)
#     success_url = reverse_lazy("auser:instructor_list_admin")
#     success_message = _("Instructor %(first_name)s %(last_name)s successfully added")


# class UpdateInstructorView(
#     PermissionRequiredMixin, SuccessMessageMixin, LogEntryChangeMixin, UpdateView
# ):
#     model = Instructor
#     template_name = "auser/instructor/instructor_update.html"
#     fields = "__all__"
#     extra_context = {"title": _("Update Instructor")}
#     permission_required = "auser.change_instructor"
#     success_message = _("Instructor %(first_name)s %(last_name)s updated successfully")

#     def get_success_url(self):
#         return reverse_lazy(
#             "auser:instructor_detail_admin", kwargs={"pk": self.object.pk}
#         )


# class DeleteInstructorView(PermissionRequiredMixin, LogEntryDeletionMixin, DeleteView):
#     model = Instructor
#     permission_required = ("auser.delete_instructor",)
#     success_url = reverse_lazy("auser:instructor_list_admin")
#     http_method_names = ["post"]


# class AddSocialMediaView(
#     PermissionRequiredMixin, SuccessMessageMixin, LogEntryAdditionMixin, CreateView
# ):
#     model = SocialMedia
#     template_name = "auser/instructor/social_media/add.html"
#     fields = "__all__"
#     extra_context = {"title": _("Add Social Media")}
#     permission_required = ("auser.add_socialmedia",)
#     success_url = reverse_lazy("auser:instructor_list_admin")
#     success_message = _("Social Media %(name)s successfully added")


# class UpdateSocialMediaView(
#     PermissionRequiredMixin, SuccessMessageMixin, LogEntryChangeMixin, UpdateView
# ):
#     model = SocialMedia
#     template_name = "auser/instructor/social_media/update.html"
#     fields = "__all__"
#     extra_context = {"title": _("Update Social Media")}
#     permission_required = ("auser.change_socialmedia",)
#     success_url = reverse_lazy("auser:instructor_list_admin")
#     success_message = _("Social Media %(name)s updated successfully")


# class DeleteSocialMediaView(PermissionRequiredMixin, LogEntryDeletionMixin, DeleteView):
#     model = SocialMedia
#     permission_required = ("auser.delete_socialmedia",)
#     success_url = reverse_lazy("auser:instructor_list_admin")
#     http_method_names = ["post"]


# class AddInstructorSocialMediaLinkView(
#     PermissionRequiredMixin, SuccessMessageMixin, LogEntryAdditionMixin, CreateView
# ):
#     model = InstructorSocialMediaLink
#     template_name = "auser/instructor/social_link/add.html"
#     fields = ("social_media", "link")
#     extra_context = {"title": _("Add Social Media Link")}
#     permission_required = ("auser.add_instructorsocialmedialink",)
#     success_message = _("Social Media Link %(social_media)s successfully added")

#     def form_valid(self, form):
#         form.instance.instructor = Instructor.objects.get(
#             pk=self.kwargs["instructor_pk"]
#         )
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy(
#             "auser:instructor_detail_admin", kwargs={"pk": self.object.instructor.pk}
#         )


# class UpdateInstructorSocialMediaLinkView(
#     PermissionRequiredMixin, SuccessMessageMixin, LogEntryChangeMixin, UpdateView
# ):
#     model = InstructorSocialMediaLink
#     template_name = "auser/instructor/social_link/update.html"
#     fields = ("social_media", "link")
#     extra_context = {"title": _("Update Social Media Link")}
#     permission_required = ("auser.change_instructorsocialmedialink",)
#     success_message = _("Social Media Link %(social_media)s updated successfully")

#     def get_success_url(self):
#         return reverse_lazy(
#             "auser:instructor_detail_admin", kwargs={"pk": self.object.instructor.pk}
#         )


# class DeleteInstructorSocialMediaLinkView(
#     PermissionRequiredMixin, LogEntryDeletionMixin, DeleteView
# ):
#     model = InstructorSocialMediaLink
#     permission_required = ("auser.delete_instructorsocialmedialink",)
#     success_url = reverse_lazy("auser:instructor_list_admin")
#     http_method_names = ["post"]

#     def get_success_url(self):
#         return reverse_lazy(
#             "auser:instructor_detail_admin", kwargs={"pk": self.object.instructor.pk}
#         )


# class AddEducationBackgroundView(
#     PermissionRequiredMixin, SuccessMessageMixin, LogEntryAdditionMixin, CreateView
# ):
#     model = EducationBackground
#     template_name = "auser/instructor/education_background/add.html"
#     form_class = EducationBackgroundForm
#     extra_context = {"title": _("Add Education Background")}
#     permission_required = ("auser.add_educationbackground",)
#     success_message = _(
#         "Education Background %(degree_level)s %(major)s successfully added"
#     )

#     def form_valid(self, form):
#         form.instance.instructor = Instructor.objects.get(
#             pk=self.kwargs["instructor_pk"]
#         )
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy(
#             "auser:instructor_detail_admin", kwargs={"pk": self.object.instructor.pk}
#         )


# class UpdateEducationBackgroundView(
#     PermissionRequiredMixin, SuccessMessageMixin, LogEntryChangeMixin, UpdateView
# ):
#     model = EducationBackground
#     template_name = "auser/instructor/education_background/update.html"
#     form_class = EducationBackgroundForm
#     extra_context = {"title": _("Update Education Background")}
#     permission_required = ("auser.change_educationbackground",)
#     success_message = _(
#         "Education Background %(degree_level)s %(major)s updated successfully"
#     )

#     def get_success_url(self):
#         return reverse_lazy(
#             "auser:instructor_detail_admin", kwargs={"pk": self.object.instructor.pk}
#         )


# class DeleteEducationBackgroundView(
#     PermissionRequiredMixin, LogEntryDeletionMixin, DeleteView
# ):
#     model = EducationBackground
#     permission_required = ("auser.delete_educationbackground",)
#     http_method_names = ["post"]

#     def get_success_url(self):
#         return reverse_lazy(
#             "auser:instructor_detail_admin", kwargs={"pk": self.object.instructor.pk}
#         )


# class AddExperienceView(
#     PermissionRequiredMixin, SuccessMessageMixin, LogEntryAdditionMixin, CreateView
# ):
#     model = Experience
#     template_name = "auser/instructor/experience/add.html"
#     form_class = ExperienceForm
#     extra_context = {"title": _("Add Experience")}
#     permission_required = ("auser.add_experience",)
#     success_message = _("Experience %(job_title)s successfully added")

#     def form_valid(self, form):
#         form.instance.instructor = Instructor.objects.get(
#             pk=self.kwargs["instructor_pk"]
#         )
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy(
#             "auser:instructor_detail_admin", kwargs={"pk": self.object.instructor.pk}
#         )


# class UpdateExperienceView(
#     PermissionRequiredMixin, SuccessMessageMixin, LogEntryChangeMixin, UpdateView
# ):
#     model = Experience
#     template_name = "auser/instructor/experience/update.html"
#     fields = "__all__"
#     extra_context = {"title": _("Update Experience")}
#     permission_required = ("auser.change_experience",)
#     success_message = _("Experience %(job_title)s updated successfully")

#     def get_success_url(self):
#         return reverse_lazy(
#             "auser:instructor_detail_admin", kwargs={"pk": self.object.instructor.pk}
#         )


# class DeleteExperienceView(PermissionRequiredMixin, LogEntryDeletionMixin, DeleteView):
#     model = Experience
#     permission_required = ("auser.delete_experience",)
#     http_method_names = ["post"]

#     def get_success_url(self):
#         return reverse_lazy(
#             "auser:instructor_detail_admin", kwargs={"pk": self.object.instructor.pk}
#         )
