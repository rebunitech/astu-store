import csv
import io
import mimetypes

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import BadRequest
from django.db.models.fields import NOT_PROVIDED
from django.http import (Http404, HttpResponse, HttpResponseBadRequest,
                         HttpResponseRedirect)
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, View  

from auser.exceptions import InvalidColumnName, LoaderException
from auser.utils import Importer


class DashboardView(LoginRequiredMixin, TemplateView):
    """Generic view for users dashboard."""

    template_name = "auser/dashboard.html"
    extra_context = {"title": _("Dashboardf")}


class ImportView(View):
    required_fields = None
    object_types = None
    date_types = None

    def get_model(self):
        """Get model."""
        if getattr(self, "model", None) is not None:
            return self.model
        try:
            ctype_pk = self.kwargs.get("pk")
            model = ContentType.objects.get(pk=ctype_pk).model_class()
        except ContentType.DoesNotExist:
            raise Http404
        return model

    def get_succuss_url(self):
        """redirect to the same page"""
        return self.request.POST.get("next", "/")

    def get_required_fields(self):
        """Get required fields."""
        if self.required_fields is None:
            self.required_fields = [
                field.name
                for field in self.get_model()._meta.fields
                if field.blank is False
                and field.default is NOT_PROVIDED
                and field.name != "password"
                and (not field.name.endswith("_ptr"))
            ]
        self.required_fields.sort()
        return self.required_fields

    def get_file(self, request):
        """Get file."""
        try:
            return request.FILES["file"]
        except KeyError:
            raise HttpResponseBadRequest(_("No file provided."))

    def get(self, request, *args, **kwargs):
        stream = io.StringIO()
        writer = csv.writer(stream)
        writer.writerow(self.get_required_fields())
        response = HttpResponse(stream.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}_template.csv".format(
            self.get_model()._meta.model_name
        )
        return response

    def post(self, request, *args, **kwargs):
        self.model = self.get_model()
        self.required_fields = self.get_required_fields()
        self.file = self.get_file(request)
        try:
            importer = Importer(
                self.file,
                self.required_fields,
                self.model,
                user_id=request.user.id,
                object_types=self.object_types,
                date_types=self.date_types,
            )
        except (LoaderException, InvalidColumnName) as error:
            messages.error(request, error)
            return HttpResponseRedirect(self.get_succuss_url())
        created_count = importer.create_objects()
        if created_count:
            messages.success(
                request,
                _("{} {} created successfully.").format(
                    created_count, self.model._meta.verbose_name_plural
                ),
            )
        else:
            messages.warning(request, _("No objects created."))
        if importer.has_invalid_data():
            messages.error(
                request, _("Some objects were not created due to invalid data.")
            )
            invalid_data_file = importer.get_invalid_file()
            invalid_data_file.name = "invalid_data.csv"
            response = HttpResponse(
                invalid_data_file.getvalue(), content_type="text/csv"
            )
            response["Content-Disposition"] = (
                "attachment; filename=%s" % invalid_data_file.name
            )
            return response

        return HttpResponseRedirect(self.get_succuss_url())

