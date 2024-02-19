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
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# First Party Imports

# Get an instance of a logger
logger = logging.getLogger(__name__)

# ______________________ Admin car List API ______________________ #


class UserCarListAPI(ListAPIView):
    """Get use car list"""

    permission_classes = [IsAuthenticated]
    serializer_class = UserCarListSerializer

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


class MileageView(APIView):
    def post(self, request, *args, **kwargs):
        car = get_object_or_404(Car, unique_key=self.kwargs["car_unique_key"])
        serializer = MileageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(car=car)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def put(self, request, *args, **kwargs):
    mileage = get_object_or_404(Mileage, unique_key=self.kwargs["unique_key"])

    serializer = MileageSerializer(mileage, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ___________________________ Admin Add Mileage API __________________________ #


# class MileageAddAPI(CreateAPIView):
#     """
#     Add a Mileage .
#     """

#     permission_classes = [IsAuthenticated]
#     serializer_class = MileageSerializer


# # ___________________________ Admin Update Destroy Mileage API __________________________ #


# class MileageUpdateAPI(RetrieveUpdateAPIView):
#     """
#     Update, Delete or Retrieve a Mileage object .
#     """

#     permission_classes = [IsAuthenticated]
#     http_method_names = ["put", "get"]
#     serializer_class = MileageSerializer

#     def put(self, request, *args, **kwargs):
#         mileage_object = self.get_object()
#         serializer = self.get_serializer(instance=mileage_object, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def get_object(self):
#         return get_object_or_404(
#             Mileage,
#             car__unique_key=self.kwargs["unique_key"],
#             created_date=Max("created_date"),
#             car__user=self.request.user,
#         )
