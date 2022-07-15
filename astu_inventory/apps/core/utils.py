import io
import os
import re

from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import NOT_PROVIDED, Model
from django.forms import modelform_factory
from django.template import loader

import pandas as pd

from astu_inventory.apps.core.exceptions import InvalidColumnName, LoaderException


def send_notification(recipients, subject, template, **kwargs):
    sender = settings.SERVER_EMAIL
    template = loader.get_template(template)
    email = EmailMessage(
        subject,
        template.render(kwargs),
        sender,
        recipients,
    )
    email.send()


class Importer:
    def __init__(
        self,
        file,
        model,
        required_fields,
        db_field_name,
        foreign_keys,
        defaults,
        validation_form=None,
        run_on_object=None,
        object_types=None,
        date_types=None,
    ):
        self.model = model
        self.required_fields = required_fields
        self.db_field_name = db_field_name
        self.validation_form = validation_form
        self.run_on_object = run_on_object
        self.defaults = defaults
        self.object_types = object_types
        self.foreign_keys = foreign_keys
        self.date_types = date_types
        self.data = self.load_data(file, object_types, date_types)
        self.valid_data, self.invalid_data = self.preprocess_data(self.data)

    def load_data(self, file, object_types=None, date_types=None):
        """
        Import data from a xlsx file.
        """
        return pd.read_excel(file, dtype=object_types, parse_dates=date_types)

    def preprocess_data(self, data):
        """
        Validate data.
        """
        if self.columns_is_valid(data.columns):
            valid_data = data.dropna(axis=0).drop_duplicates()
            invalid_data = data[~data.index.isin(valid_data.index)]
            return valid_data, invalid_data

    def columns_is_valid(self, columns):
        """
        Validate columns.
        """
        required_fields = pd.Series(self.required_fields)
        if not required_fields.isin(columns).all():
            raise InvalidColumnName(
                "Invalid column name %(names)s are required"
                % {"names": ", ".join([field for field in required_fields[~required_fields.isin(columns)]])}
            )
        return True

    def create_objects(self):
        """
        Create objects from valid data.
        """
        if self.validation_form is None:
            self.validation_form = modelform_factory(self.model, fields=self.db_field_name)
        field_map = dict(zip(self.db_field_name, self.required_fields))
        created = 0
        for index, row in self.valid_data.iterrows():
            data = dict(zip(self.db_field_name, row))

            for attr, value in self.defaults.items():
                data.setdefault(attr, value)

            for field, resolver in self.foreign_keys.items():
                if callable(resolver):
                    data[field] = resolver(data[field])
                else:
                    model, attr = resolver
                    data[field] = model.objects.get(**{attr: data[field]})

            form = self.validation_form(data)
            if form.is_valid():
                obj = form.save()
                if self.run_on_object is not None:
                    self.run_on_object(obj)
                created += 1
            else:
                row["error"] = "\n".join(
                    [
                        "%s : " % field_map.get(field, field) + "\n".join(errors)
                        for field, errors in form.errors.items()
                    ]
                )
                if self.invalid_data.shape[0] == 0:
                    self.invalid_data.columns = self.data.columns
                self.invalid_data = self.invalid_data.append(pd.DataFrame(row).T)

        return created

    def has_invalid_data(self):
        return self.invalid_data.shape[0] > 0

    def get_invalid_file(self):
        stream = io.StringIO()
        self.invalid_data.to_csv(stream, index=False)
        return stream
