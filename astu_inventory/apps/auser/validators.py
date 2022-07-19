""" ASTU Inventory validators list

    Date Created: 3 July, 2022
    Author: Wendirad Demelash(@wendirad)
"""

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class PhoneNumberValidator(RegexValidator):
    """Phone number validator, used to validate both local and international
    phone number formats, and also accept 3 digit service numbers.

    Attributes:
        regex: regeular expression that represent phone number replace super class default empty value.
        message: message to be displayed if validation fail.
        code: code name used to identify error when raises.
    """

    regex = r"^((\+2519|09)\d{8})$|(\+251\d{3})$"
    message = _("Please enter your phone number in +2519********" " or 09******** format.")
    code = "invalid_phone_number"


class ShortNameValidator(RegexValidator):
    """Short  name validator, used to validate departments short name"""

    regex = r"^[a-zA-Z0-9\_\-]+$"
    message = _("Short name must not containt other than capital letters, small letters, digits, _ or -.")
    code = "invalid_short_name"
