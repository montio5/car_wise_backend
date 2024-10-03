# Standard Library
import enum

# Django
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class AppMessages(enum.Enum):
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
    RESET_CODE_SENT_MSG = _("Code sent to your email")
    PASSWORD_RESET_ENABLED_MSG = _("Password reset enabled")
    PASSWORD_UPDATED_SUCCESS_MSG = _("Password updated successfully")
    CAR_NOTIFICATION = _("{} has {} elements ")
    CHECK_NOTIFICATION = _(" to check based on estimated mileage.")
    NO_MESSAGE = _("checked. There is nothing to update.")
    YOUR_RESET_PASSWORD = _("Your password reset code is:")
    USE_CODE_FOR_REST_PASS = _(
        "Please use this code to reset your password. The code will expire in 5 minutes."
    )
    FORGOT_PASSWORD = _("Forgot Password")
    PAST = _("{} ago updated")
    # Errors
    CURRENT_PASSWORD_IS_INCORRECT = _("Current password is incorrect.")
    USER_NOT_FOUND_MSG = _("User not found")
    RESET_CODE_NOT_FOUND_MSG = _("Reset code not found")
    RESET_CODE_EXPIRED_MSG = _("The code is expired")
    RESET_CODE_INVALID_MSG = _("Invalid code")
    PASSWORD_DO_NOT_MATCH = _("New password and its repeat do not match.")
    INVALID_UPDATE_MILEAGE = _("{} cannot be lower than the previous mileage.")
    MAX_CAR_ERROR = _(
        "You can not add more than {} cars in an account in free version".format(
            settings.ALLOWED_CAR_AMOUNT
        )
    )
    INVALID_CUSTOM_FIELD = _(
        "Invalid custom field! one of the fields should be filled. fields are :{}"
    )
    MUST_FIELD = _("{} should filed!")
    BOTH_MUST_FIELD = _("Both {} and {} should filed!")
    AT_LAST_ONE_FIELD_SHOULD_FILLED = _("At last one section should be filled!")

    CAN_NOT_GREATER_THAN_MILEAGE = _(
        "The field {} is greater than mileage you entered!"
    )
    SHOULD_BE_POSETIVE_INTEGER = _("The field {} Should be greater than 0!")
    LAST_CHABGED_DATE_CANT_BE_IN_FUTURE = _("Last changed date can't be in future")
    USER_EXISTS = _("This email is taken!")
