import io
import os
import re

import pandas as pd
from django.utils.translation import gettext_lazy as _

from auser.exceptions import InvalidColumnName, LoaderException
from auser.signals import log_entry_adition


def generate_username(length=6):
    """Generate a random username of length 10."""
    return os.urandom(length // 2).hex()


class Importer:
    """
    A class which used to import data from a csv/xlsx file. used to preprocess and validate data.
    """

    def __init__(
        self, file, required_fields, model, user_id, object_types=None, date_types=None
    ):
        """
        Initialize the class.
        """
        self.file = file
        self.model = model
        self.user_id = user_id
        self.date_types = date_types
        self.object_types = object_types
        self.required_fields = required_fields
        self.data = self.load_data(file, object_types, date_types)
        self.valid_data, self.invalid_data = self.preprocess_data(self.data)

    def load_data(self, file, object_types=None, date_types=None):
        """
        Import data from a csv/xlsx file.
        """
        if file.name.endswith(".csv"):
            data = pd.read_csv(file, dtype=object_types, parse_dates=date_types)
        elif file.name.endswith(".xlsx"):
            data = pd.read_excel(file, dtype=object_types, parse_dates=date_types)
        else:
            raise LoaderException(_("File type not supported."))
        return data

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
                _("Invalid column name %(names)s are required")
                % {
                    "names": ", ".join(
                        [
                            field
                            for field in required_fields[~required_fields.isin(columns)]
                        ]
                    )
                }
            )
        return True

    def get_error_detail(self, error):
        pattern = r"DETAIL: (?P<error_msg>.+)"
        if re.search(pattern, str(error)):
            return re.search(pattern, str(error)).group("error_msg")
        return str(error)

    def create_objects(self):
        """
        Create objects from valid data.
        """
        created = 0
        for index, row in self.valid_data.iterrows():
            try:
                obj = self.model.objects.create(**row)
                log_entry_adition.send(
                    sender=self.model,
                    instance=obj,
                    user_id=self.user_id,
                    created=True,
                )
                created += 1
            except Exception as error:
                row["error"] = self.get_error_detail(error)
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
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         import io
import os
import re

import pandas as pd
from django.utils.translation import gettext_lazy as _

from auser.exceptions import InvalidColumnName, LoaderException
from auser.signals import log_entry_adition


def generate_username(length=6):
    """Generate a random username of length 10."""
    return os.urandom(length // 2).hex()


class Importer:
    """
    A class which used to import data from a csv/xlsx file. used to preprocess and validate data.
    """

    def __init__(
        self, file, required_fields, model, user_id, object_types=None, date_types=None
    ):
        """
        Initialize the class.
        """
        self.file = file
        self.model = model
        self.user_id = user_id
        self.date_types = date_types
        self.object_types = object_types
        self.required_fields = required_fields
        self.data = self.load_data(file, object_types, date_types)
        self.valid_data, self.invalid_data = self.preprocess_data(self.data)

    def load_data(self, file, object_types=None, date_types=None):
        """
        Import data from a csv/xlsx file.
        """
        if file.name.endswith(".csv"):
            data = pd.read_csv(file, dtype=object_types, parse_dates=date_types)
        elif file.name.endswith(".xlsx"):
            data = pd.read_excel(file, dtype=object_types, parse_dates=date_types)
        else:
            raise LoaderException(_("File type not supported."))
        return data

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
                _("Invalid column name %(names)s are required")
                % {
                    "names": ", ".join(
                        [
                            field
                            for field in required_fields[~required_fields.isin(columns)]
                        ]
                    )
                }
            )
        return True

    def get_error_detail(self, error):
        pattern = r"DETAIL: (?P<error_msg>.+)"
        if re.search(pattern, str(error)):
            return re.search(pattern, str(error)).group("error_msg")
        return str(error)

    def create_objects(self):
        """
        Create objects from valid data.
        """
        created = 0
        for index, row in self.valid_data.iterrows():
            try:
                obj = self.model.objects.create(**row)
                log_entry_adition.send(
                    sender=self.model,
                    instance=obj,
                    user_id=self.user_id,
                    created=True,
                )
                created += 1
            except Exception as error:
                row["error"] = self.get_error_detail(error)
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
