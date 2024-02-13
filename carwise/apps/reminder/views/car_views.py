# Standard Library
import logging
from apps.reminder.models import Car, Mileage

# Django
from apps.reminder.serializers.car_serializers import (
    CarSerializer,
    MileageSerializer,
    UserCarListSerializer,
)
from django.db.models import Max

# Third Party Packages
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

# First Party Imports
from drf_yasg import openapi

# Get an instance of a logger
logger = logging.getLogger(__name__)

# ______________________ Admin car List API ______________________ #


class UserCarListAPI(ListAPIView):
    """Get use car list"""

    permission_classes = [IsAuthenticated]
    serializer_class = UserCarListSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve Album List",
        operation_description="Get Album list.",
        manual_parameters=[
            openapi.Parameter(
                "Accept-Language",
                openapi.IN_HEADER,
                description="Choose language from the sandbox",
                type=openapi.TYPE_STRING,
                enum=["EN", "DE"],
                default="DE",
            ),
        ],
        responses={
            status.HTTP_200_OK: UserCarListSerializer,
            status.HTTP_401_UNAUTHORIZED: "Unauthorized, if credentials were not provided.",
            status.HTTP_405_METHOD_NOT_ALLOWED: "Method Not Allowed, if wrong HTTP method was used; e.g. PUT instead of GET.",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "An unexpected error occurred.",
        },
        tags=["public_gallery"],
    )
    def get_queryset(self):
        user = self.request.user
        return user.user_cars.all()


# ___________________________ Admin Add car API __________________________ #


class CarAddAPI(CreateAPIView):
    """
    Add an car .
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CarSerializer


# ___________________________ Admin Update Destroy car API __________________________ #


class CarUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    """
    Update, Delete or Retrieve a car object .
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["put", "delete", "get"]
    serializer_class = CarSerializer

    def put(self, request, *args, **kwargs):
        car_object = self.get_object()
        serializer = self.get_serializer(instance=car_object, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        return get_object_or_404(
            Car,
            unique_key=self.kwargs["unique_key"],
        )


# ___________________________ Admin Add Mileage API __________________________ #


class MileageAddAPI(CreateAPIView):
    """
    Add a Mileage .
    """

    permission_classes = [IsAuthenticated]
    serializer_class = MileageSerializer


# ___________________________ Admin Update Destroy Mileage API __________________________ #


class MileageUpdateAPI(RetrieveUpdateAPIView):
    """
    Update, Delete or Retrieve a Mileage object .
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["put", "get"]
    serializer_class = MileageSerializer

    def put(self, request, *args, **kwargs):
        mileage_object = self.get_object()
        serializer = self.get_serializer(instance=mileage_object, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        return get_object_or_404(
            Mileage,
            car__unique_key=self.kwargs["unique_key"],
            created_date=Max("created_date"),
            car__user=self.request.user,
        )
