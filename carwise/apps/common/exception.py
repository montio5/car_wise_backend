# Django
from django.utils.translation import gettext_lazy as _

# Third Party Packages
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError, _get_error_details

# First Party Imports
from apps.common.message import AppMessages

class InternalServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = AppMessages.CONTACT_ADMINISTRATOR.value
    default_code = "internal-server-error"


class TokenError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Token is invalid or expired")
    default_code = "invalid-token"


class ProtectedError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _(
        "This item cannot be deleted because it is being used by other rows."
    )
    default_code = "cannot-delete-item"

class MyIntegrityError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Duplicate key value violates unique constraint.")
    default_code = "violates-unique-constraint"