# Standard Library
import logging

# First Party Imports
# from apps.common.firebase import send_fcm_notification
from apps.common.firebase import  send_push_notification
from apps.reminder.serializers.custom_serializers import (
    CustomFieldSerializer,
    CustomSetupSerializer,
)
from apps.reminder.models import Car, CarCustomSetup, CustomFiled

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
from drf_spectacular.utils import extend_schema


# Get an instance of a logger
logger = logging.getLogger(__name__)

# ______________________ Custom Field List API ______________________ #


@extend_schema(tags=["custom-field"])
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


# ___________________________ Custom Field Add API __________________________ #


@extend_schema(tags=["custom-field"])
class CustomFieldAddAPI(CreateAPIView):
    """
    Add a car .
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CustomFieldSerializer

    def post(self, request, *args, **kwargs):
        car = self.get_object()
        serializer_context = {"car_object": car}
        serializer = self.get_serializer(data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save(car=car)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_object(self):
        user = self.request.user
        return get_object_or_404(
            Car, unique_key=self.kwargs["car_unique_key"], user=user
        )


# ___________________________ Custom Field Update Destroy API __________________________ #


@extend_schema(tags=["custom-field"])
class CustomFieldUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    """
    Update, Delete or Retrieve a car object .
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["put", "delete", "get"]
    serializer_class = CustomFieldSerializer

    def put(self, request, *args, **kwargs):
        custom_field_object = self.get_object()
        serializer_context = {"car_object": custom_field_object.car}
        serializer = self.get_serializer(
            instance=custom_field_object, data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # TODO: remove after test

        send_push_notification(
            request.user,
            "a new custom field",
            "a new custom field is added successfully",
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        return get_object_or_404(
            CustomFiled, id=self.kwargs["id"], car__user=self.request.user
        )


# ___________________________ Car Custom Setup Update Destroy API __________________________ #


@extend_schema(tags=["custom-setup"])
class CarCustomSetupUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    """
    Update, Delete or Retrieve a car object .
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["put", "get", "delete"]
    serializer_class = CustomSetupSerializer

    def put(self, request, *args, **kwargs):
        car_object = self.get_object()
        serializer = self.get_serializer(instance=car_object, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        car_object = get_object_or_404(Car, unique_key=self.kwargs["car_unique_key"], user=self.request.user)
        
        # Delete the existing CarCustomSetup object if it exists
        try:
            existing_setup = CarCustomSetup.objects.get(car=car_object)
            existing_setup.delete()
            CarCustomSetup.objects.create(car=car_object)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except CarCustomSetup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

    def get_object(self):
        return get_object_or_404(
            CarCustomSetup,
            car__unique_key=self.kwargs["car_unique_key"],
            car__user=self.request.user,
        )
