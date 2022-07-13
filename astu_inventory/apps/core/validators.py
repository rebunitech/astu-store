import datetime

from django.conf import settings
from django.core.exceptions import ValidationError

import pytz

tzinfo = pytz.timezone(settings.TIME_ZONE)


def validate_past(date):
    if date.date() < datetime.datetime.today().replace(tzinfo=tzinfo).date():
        raise ValidationError("Date cannot be in the past")
