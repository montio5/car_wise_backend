# Standard Library
import logging

# Django
from django.core.exceptions import PermissionDenied as CorePermissionDenied
from django.db import IntegrityError
from django.db.models import ProtectedError as CoreProtectedError
from django.http import Http404
from django.utils import translation
from django.utils.translation import lazy

# Third Party Packages
from rest_framework import exceptions, views
from rest_framework.exceptions import APIException, ErrorDetail
from rest_framework.response import Response

# First Party Imports
from apps.common.exception import InternalServerError, MyIntegrityError, ProtectedError

logger = logging.getLogger(__name__)

from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_response = {
            'error': str(exc),
        }
        response.data = custom_response

    return response

def django_exception_handler(exc, context):
    """This function is a wrapper on views.exception_handler"""

    def translate_exc(e):
        if isinstance(e, Http404):
            return exceptions.NotFound()
        if isinstance(e, CorePermissionDenied):
            return exceptions.PermissionDenied()
        return e

    response = views.exception_handler(exc, context)
    return translate_exc(exc), (dict(response.items()) if response else None)


class ExceptionHandler:
    """The main exception handler class for whole system."""

    def __call__(self, exc, context, *args, **kwargs):
        return self._handle_exception(exc, context)

    def _handle_exception(self, exc, context):
        trace_id = getattr(context.get("request"), "id", "NO_TRACE_ID")

        exc, headers = django_exception_handler(exc, context)

        if isinstance(exc, APIException):
            with translation.override("en"):
                logger.error(lazy(str)(exc))
            return self._create_response(lazy(str)(exc), headers=headers, trace_id=trace_id)

        with translation.override("en"):
            logger.exception(lazy(str)(exc))

        if isinstance(exc, CoreProtectedError):
            return self._create_response(ProtectedError(), trace_id=trace_id)

        if isinstance(exc, IntegrityError):
            return self._create_response(MyIntegrityError(), trace_id=trace_id)

        return self._create_response(InternalServerError(detail=exc), trace_id=trace_id)

    def _create_response(self, e: APIException, headers=None, trace_id=-1):
        body = {
            "status_code": e.status_code,
            "detail": self.make_fields_errors(e.detail),
            "general_error": self.make_general_error(e.detail),
            "trace_id": trace_id,
        }
        return Response(body, status=e.status_code, headers=headers or {})

    def make_general_error(self, detail):
        if isinstance(detail, str):
            return {"msg": detail}
        return {}

    def make_fields_errors(self, detail):
        if isinstance(detail, dict):
            return {k: self.make_errors(v) for k, v in detail.items()}
        return {}

    def make_errors(self, detail):
        if isinstance(detail, list):
            return [self.make_error(item) for item in detail if bool(item)]

        if isinstance(detail, dict):
            if "non_field_errors" in detail:
                return [
                    self.make_error(item)
                    for item in detail["non_field_errors"]
                    if bool(item)
                ]
            return self.make_fields_errors(detail)

        if isinstance(detail, ErrorDetail):
            return [self.make_error(detail)]
        return []

    def make_error(self, detail):
        if isinstance(detail, ErrorDetail):
            return self.make_error_obj(detail.code, str(detail))
        try:
            return self.make_error_obj(
                detail["non_field_errors"][0].code, str(detail["non_field_errors"][0])
            )
        except KeyError:
            return self.make_error_obj("error", detail)

    def make_error_obj(self, code, msg):
        return {"code": code, "msg": msg}


custom_exception_handler = ExceptionHandler()
