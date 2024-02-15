# Django
from django.conf import settings
from django.utils import timezone

# Third Party Packages
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.common.message import AppMessages

from apps.reminder.models import Car, CarCompany, CustomFiled, Mileage, CarModel
from apps.reminder.serializers.custom_serializers import CustomFieldSerializer

# First Party Imports

# __________________  Car List Serializer ___________________ #


class UserCarListSerializer(serializers.ModelSerializer):
    """serializer for getting list of cars"""

    unique_key = serializers.CharField(read_only=True)
    car_model = serializers.CharField(source="car_model.name")
    car_company = serializers.CharField(source="car_model.car_company.name")

    class Meta:
        model = Car
        fields = [
            "unique_key",
            "name",
            "car_company",
            "car_model",
        ]


# __________________  Custom Field List Serializer ___________________ #


class CustomFieldListSerializer(serializers.ModelSerializer):
    """serializer for getting, updating custom_field detail"""

    class Meta:
        model = CustomFiled
        fields = "__all__"


# __________________  Car Serializer ___________________ #


class CarSerializer(serializers.ModelSerializer):
    """serializer for getting, updating cars detail"""

    car_model = serializers.PrimaryKeyRelatedField(
        queryset=CarModel.objects.all(),
        required=True,
    )

    class Meta:
        model = Car
        fields = [
            "car_model",
            "name",
        ]

    def create(self, validated_data):
        car = Car.objects.create(
            **validated_data, user=self.context.get("request").user
        )
        return car

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# __________________  Mileage Serializer ___________________ #


class MileageSerializer(serializers.ModelSerializer):
    """serializer for getting, updating mileage detail"""

    car = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(),
        required=True,
    )
    created_date = serializers.DateTimeField(read_only=True)
    unique_key = serializers.CharField(read_only=True)
    custom_fields = CustomFieldSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Mileage
        fields = ["car", "created_date", "unique_key", "custom_fields"]
        read_only_fields = ["unique_key", "created_date"]

    def validate(self, object):
        if object.car in Car.objects.filter(user=self.context.get("request").user):
            raise ValidationError(AppMessages.NOT_ALOWED_TO_CHANGE.value)
        return object

    def create(self, validated_data):
        validated_data.pop("created_date", None)
        validated_data.pop("unique_key", None)
        mileage = Mileage.objects.create(**validated_data)
        return mileage

    def update(self, instance, validated_data):
        validated_data.pop("created_date", None)
        validated_data.pop("unique_key", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
