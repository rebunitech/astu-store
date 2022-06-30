import datetime

import pytz
from django.core.exceptions import ValidationError

utc = pytz.UTC


def validate_past(date):
    if date < datetime.datetime.today().replace(tzinfo=utc):
        raise ValidationError("Date cannot be in the past")
