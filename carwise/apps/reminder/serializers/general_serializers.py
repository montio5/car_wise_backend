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

    car_models = serializers.SerializerMethodField()

    class Meta:
        model = CarCompany
        fields = ["id", "name", "car_models"]

    def get_car_models(self, obj):
        # Retrieve the car models and sort them by any field, such as name
        car_models = obj.carmodel_set.all().order_by(
            "name"
        )
        return CarModelListSerializer(car_models, many=True).data
