# Django

# Third Party Packages
from rest_framework import serializers

from apps.reminder.models import (
    CarCompany,
    CarModel,
)

# __________________  Car Model List Serializer ___________________ #


class CarModelListSerializer(serializers.ModelSerializer):
    """serializer for getting car models"""

    class Meta:
        model = CarModel
        fields = [
            "id",
            "name",
        ]


# __________________  Car Company List Serializer ___________________ #


class CarCompanyListSerializer(serializers.ModelSerializer):
    """serializer for getting car companies"""

    car_models = CarModelListSerializer(
        many=True, read_only=True, source="carmodel_set"
    )

    class Meta:
        model = CarCompany
        fields = ["id", "name", "car_models"]
