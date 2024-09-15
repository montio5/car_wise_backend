# Standard Library
import logging

from django.http import HttpResponseNotFound

# First Party Imports
from apps.reminder.models import Car
from apps.reminder.serializers.car_serializers import (
    CarSerializer,
    MileageSerializer,
    UserCarListSerializer,
)
# Third Party Packages
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


# Get an instance of a logger
logger = logging.getLogger(__name__)

# ______________________ car List API ______________________ #


@extend_schema(tags=["car"])
class UserCarListAPI(ListAPIView):
    """Get use car list"""

    permission_classes = [IsAuthenticated]
    serializer_class = UserCarListSerializer

    def get_queryset(self):
        user = self.request.user
        return user.user_cars.all()


# ___________________________ Admin Add car API __________________________ #


@extend_schema(tags=["car"])
class CarAddAPI(CreateAPIView):
    """
    Add an car .
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CarSerializer


# ___________________________ Update Destroy Car API __________________________ #


@extend_schema(tags=["car"])
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
            Car, unique_key=self.kwargs["unique_key"], user=self.request.user
        )


# ___________________________  Add/Update Mileage API __________________________ #


@extend_schema(tags=["mileage"])
class MileageView(CreateAPIView, UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MileageSerializer
    http_method_names = ["put", "post", "get"]
    
    def get_object(self):
        return get_object_or_404(
            Car, unique_key=self.kwargs["unique_key"], user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(car=self.get_object())

    def perform_update(self, serializer):
        serializer.save()

    def get(self, request, *args, **kwargs):
        car = self.get_object()
        mileage = car.car_mileages.all().order_by("-created_date").first()
        if mileage:
            serializer = MileageSerializer(instance=mileage)
            return Response(serializer.data)
        return HttpResponseNotFound()
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["car"] = self.get_object()
        return context
