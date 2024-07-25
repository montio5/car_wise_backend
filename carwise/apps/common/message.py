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
    BOTH_MUST_FIELD = _("Both {} and {} should filed!")
    AT_LAST_ONE_FIELD_SHOULD_FILLED = _("At last one section should be filled!")

    CAN_NOT_GREATER_THAN_MILEAGE = _(
        "The field {} is greater than mileage you entered!"
    )
    USER_EXISTS = _("This email is taken!")
    INVALID_UPDATE_MILEAGE = _("{} cannot be lower than the previous mileage.")

    CHECK_FIELD_MILEAGE = _("Your {} is overdue for replacement based on mileage.")
    CHECKER_FIELD_DATE = _(
        "It's been a considerable amount of time since your last {} change."
    )
    CHECK_PLEASE_MESSAGE = _("Please check {} . long time no check!")
    DATE_PASSED = _("{} passed!")
    DATE_FUTURE = _("next {}")
    YEAR = _("{} year(s)")
    MONTH = _("{} month(s)")
    DAY = _("{} day(s)")
    OVERDUE = _("overdue")
    AND = _("and")
    COMMA = _(",")
