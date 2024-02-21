# Standard Library
import enum

# Django
from django.utils.translation import gettext_lazy as _


class AppMessages(enum.Enum):
    NOT_ALOWED_TO_CHANGE = _(" you are not alowed to change this car mileage")
    INVALID_CUSTOM_FIELD = _(
        "Invalid custom field! one of the fields should be filled. fields are :{}"
    )
    MUST_FIELD = _("{} should filed!")
    CAN_NOT_GREATER_THAN_MILEAGE = _(
        "The field {} is greater than mileage you entered!"
    )
