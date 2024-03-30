import logging
from django.core.exceptions import PermissionDenied as CorePermissionDenied
from django.db import IntegrityError
from django.db.models import ProtectedError as CoreProtectedError
from django.http import Http404
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, views
from rest_framework.exceptions import APIException, ErrorDetail
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class ExceptionHandler:
    """The main exception handler class for the whole system."""

    def __call__(self, exc, context, *args, **kwargs):
        return self._handle_exception(exc, context)

    def _handle_exception(self, exc, context):
        trace_id = getattr(context.get("request"), "id", "NO_TRACE_ID")

        exc, headers = self.django_exception_handler(exc, context)

        if isinstance(exc, APIException):
            with translation.override("en"):
                logger.error(str(exc))
            return self._create_response(
                exc, headers=headers, trace_id=trace_id  # Pass exc instead of str(exc)
            )

        with translation.override("en"):
            logger.exception(str(exc))

        if isinstance(exc, CoreProtectedError):
            return self._create_response(_("Protected error"), trace_id=trace_id)

        if isinstance(exc, IntegrityError):
            return self._create_response(_("Integrity error"), trace_id=trace_id)

        # Treat other exceptions (string errors) as internal server errors
        return self._create_response(
            _("Internal server error"), status_code=500, trace_id=trace_id
        )

    def _create_response(
        self, e: APIException, headers=None, status_code=None, trace_id=-1
    ):
        if status_code is None:
            status_code = e.status_code if isinstance(e, APIException) else 500

        body = {
            "status_code": status_code,
            "detail": self.make_fields_errors(e.detail),
            "general_error": self.make_general_error(e.detail),
            "trace_id": trace_id,
        }
        return Response(body, status=status_code, headers=headers or {})

    def django_exception_handler(self, exc, context):
        """This function is a wrapper on views.exception_handler"""

        def translate_exc(e):
            if isinstance(e, Http404):
                return exceptions.NotFound()
            if isinstance(e, CorePermissionDenied):
                return exceptions.PermissionDenied()
            return e

        response = views.exception_handler(exc, context)
        return translate_exc(exc), (dict(response.items()) if response else None)

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


# Instantiate the ExceptionHandler class
custom_exception_handler = ExceptionHandler()
