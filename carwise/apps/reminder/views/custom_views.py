# Standard Library
import logging
from apps.reminder.models import Car, CarCustomSetup, CustomFiled, Mileage

# Django
from apps.reminder.serializers.car_serializers import (
    CarSerializer,
)

# Third Party Packages
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# First Party Imports
from apps.reminder.serializers.custom_serializers import CustomFieldSerializer
from rest_framework.decorators import api_view

# Get an instance of a logger
logger = logging.getLogger(__name__)

# ______________________ Custom Field List API ______________________ #


class CustomFieldListAPI(ListAPIView):
    """Get use car list"""

    permission_classes = [IsAuthenticated]
    serializer_class = CustomFieldSerializer

    def get_queryset(self):
        car_unique_key = self.kwargs["car_unique_key"]
        user = self.request.user
        return CustomFiled.objects.filter(
            car__unique_key=car_unique_key, car__user=user
        )


# ___________________________ Admin Add car API __________________________ #


class CustomFieldAddAPI(CreateAPIView):
    """
    Add an car .
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CustomFieldSerializer


# ___________________________ Admin Update Destroy car API __________________________ #


class CustomFieldUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    """
    Update, Delete or Retrieve a car object .
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["put", "delete", "get"]
    serializer_class = CustomFieldSerializer

    def put(self, request, *args, **kwargs):
        car_object = self.get_object()
        serializer = self.get_serializer(instance=car_object, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        return get_object_or_404(
            CustomFiled,
            unique_key=self.kwargs["id"],
        )


# ___________________________ Car Custom Setup Update Destroy API __________________________ #


class CarCustomSetupUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    """
    Update, Delete or Retrieve a car object .
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["put", "get"]
    serializer_class = CarSerializer

    def put(self, request, *args, **kwargs):
        car_object = self.get_object()
        serializer = self.get_serializer(instance=car_object, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        return get_object_or_404(
            CarCustomSetup,
            car__unique_key=self.kwargs["car_unique_key"],
        )
