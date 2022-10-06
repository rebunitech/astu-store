import io

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import BadRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, View

import xlsxwriter

from astu_inventory.apps.core.exceptions import InvalidColumnName, LoaderException
from astu_inventory.apps.core.utils import Importer
from astu_inventory.apps.inventory.models import Product


class ListAvailableProductsView(PermissionRequiredMixin, ListView):
    model = Product
    context_object_name = "products"
    permission_required = "core.can_list_available_product"
    extra_context = {"title": "Products"}
    template_name = "core/product_list.html"
    paginated_by = 50

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .values(
                "name",
                "slug",
                "availables",
                "critical_no",
                "category__name",
                "sub_category__name",
                "department__short_name",
                "measurment__name",
            )
        )


class ImportView(View):
    file_name_prefix = None  # default to model name
    file_request_kwarg = "file"
    object_types = None
    date_types = None
    validation_form = None
    formats = {}
    defaults = {}
    foreign_keys = {}
    choices_list_work_sheet_name = None

    def get_file(self, request):
        try:
            return request.FILES[self.file_request_kwarg]
        except KeyError:
            raise BadRequest("No file provided.")

    def set_formats(self, workbook):
        for field in self.db_field_name:
            if hasattr(self, "get_%s_format" % field):
                format_ = getattr(self, "get_%s_format" % field)(workbook)
                self.formats[field] = format_

    def add_validation(self, worksheet):
        pass

    def write_choice_form_list(self, items, worksheet, column, start_row=0):
        item_count = 0
        for ix, choice in enumerate(items):
            item_count += 1
            worksheet.write(start_row + ix, column, choice)
        return item_count

    def get_foreign_keys(self):
        return self.foreign_keys

    def get_defaults(self):
        return self.defaults

    def _get_callable(self):
        if hasattr(self, "run_on_object"):
            return self.run_on_object

    def get(self, request, *args, **kwargs):
        stream = io.BytesIO()
        workbook = xlsxwriter.Workbook(stream)
        worksheet = workbook.add_worksheet()
        if self.choices_list_work_sheet_name is not None:
            choices_worksheet = workbook.add_worksheet(self.choices_list_work_sheet_name)
            self.write_choices(choices_worksheet)
            choices_worksheet.hide()

        self.set_formats(workbook)
        self.add_validation(worksheet)
        for ix, field in enumerate(self.required_fields):
            worksheet.set_column(ix, ix, None, self.formats.get(self.db_field_name[ix]))
            worksheet.write(0, ix, field)
        workbook.close()
        response = HttpResponse(stream.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}_template.xlsx".format(
            self.file_name_prefix or self.model._meta.model_name
        )
        return response

    def post(self, request, *args, **kwargs):
        file = self.get_file(request)
        try:
            importer = Importer(
                file,
                self.model,
                self.required_fields,
                self.db_field_name,
                self.get_foreign_keys(),
                self.get_defaults(),
                validation_form=self.validation_form,
                run_on_object=self._get_callable(),
                object_types=self.object_types,
            )
        except (LoaderException, InvalidColumnName) as error:
            messages.error(request, error)
            return HttpResponseRedirect(self.success_url)

        created_count = importer.create_objects()

        if created_count:
            messages.success(
                request,
                "{} {} created successfully.".format(created_count, self.model._meta.verbose_name_plural),
            )
        else:
            messages.warning(request, "No objects created.")

        if importer.has_invalid_data():
            messages.error(request, "Some objects were not created due to invalid data.")
            invalid_data_file = importer.get_invalid_file()
            invalid_data_file.name = "invalid_data.csv"
            response = HttpResponse(invalid_data_file.getvalue(), content_type="text/csv")
            response["Content-Disposition"] = "attachment; filename=%s" % invalid_data_file.name
            return response

        return HttpResponseRedirect(self.success_url)
