# Django
from django.conf import settings
from django.utils import timezone
import secrets

# Third Party Packages
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.common.message import AppMessages

from apps.reminder.models import (
    Car,
    CarCompany,
    CarCustomSetup,
    CustomFiled,
    Mileage,
    CarModel,
)
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


# __________________  Mileage Serializer ___________________ #


class MileageSerializer(serializers.ModelSerializer):
    """serializer for getting, updating mileage detail"""

    unique_key = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(format="%d.%m.%Y", read_only=True)

    class Meta:
        model = Mileage
        exclude = ["car"]

    def validate(self, validated_data):
        mileage = validated_data.get("mileage")
        if mileage is not None:
            for field_name in validated_data:
                if (
                    isinstance(validated_data[field_name], int)
                    and validated_data[field_name] > mileage
                ):
                    raise ValidationError(
                        AppMessages.CAN_NOT_GREATER_THAN_MILEAGE.value.format(
                            field_name
                        )
                    )
        car = self.context.get("car", None)
        if car is None:
            return validated_data
        # check the entered amount not less than previous
        previous_mileages = Mileage.objects.filter(car=car.id).order_by("-created_date")
        # breakpoint()
        if previous_mileages:
            previous_mileage = previous_mileages.first()
            for field_name, field_value in validated_data.items():
                # Check if the field is an integer and exists in the previous mileage object
                if isinstance(field_value, int) and hasattr(
                    previous_mileage, field_name
                ):
                    # Get the corresponding field value from the previous mileage object
                    previous_field_value = getattr(previous_mileage, field_name)
                    if isinstance(previous_field_value, int):
                        # Compare the field values
                        if field_value < previous_field_value:
                            raise serializers.ValidationError(
                                AppMessages.INVALID_UPDATE_MILEAGE.value.format(
                                    field_name
                                )
                            )

        return validated_data

    def create(self, validated_data):
        car = validated_data.get("car")
        last_mileage = Mileage.objects.filter(car=car).order_by("-created_date")
        if last_mileage:
            cloned_instance = Mileage.objects.get(pk=last_mileage.first().id)
            cloned_instance.pk = None  # Reset primary key to create a new object
            cloned_instance.unique_key = secrets.token_urlsafe(32)

            for attr, value in validated_data.items():
                setattr(cloned_instance, attr, value)
            cloned_instance.save()
            return cloned_instance
        return super().create(validated_data)


# __________________  Car Serializer ___________________ #


class CarSerializer(serializers.ModelSerializer):
    """serializer for getting, updating cars detail"""

    unique_key = serializers.CharField(read_only=True)
    car_model = serializers.PrimaryKeyRelatedField(
        queryset=CarModel.objects.all(),
        required=True,
    )
    car_model_display = serializers.CharField(read_only=True, source="car_model.name")
    mileage_info = MileageSerializer(required=True, write_only=True)
    custom_fields = CustomFieldSerializer(
        many=True, read_only=True, source="car_custom_fileds"
    )

    class Meta:
        model = Car
        fields = [
            "unique_key",
            "car_model",
            "car_model_display",
            "name",
            "mileage_info",
            "custom_fields",
        ]

    def create(self, validated_data):
        mileage_info = validated_data.pop("mileage_info", None)
        car = Car.objects.create(
            **validated_data, user=self.context.get("request").user
        )
        if mileage_info:
            Mileage.objects.create(car=car, **mileage_info)  # Create Mileage object
        CarCustomSetup.objects.create(car=car)
        return car

    def update(self, instance, validated_data):
        mileage_info = validated_data.pop("mileage_info", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # edit milage
        if mileage_info:
            mileage_instance = (
                Mileage.objects.filter(car=instance).order_by("-created_date").first()
            )

            for attr, value in mileage_info.items():
                setattr(mileage_instance, attr, value)
            mileage_instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        last_mileage = instance.car_mileages.order_by("-created_date").first()
        data["mileage_info"] = {}
        if last_mileage is not None:
            data["mileage_info"] = MileageSerializer(last_mileage).data
        return data

    # def validate(self, object):
    #     if object.car in Car.objects.filter(user=self.context.get("request").user):
    #         raise ValidationError(AppMessages.NOT_ALOWED_TO_CHANGE.value)
    #     return object

    # def create(self, validated_data):
    #     validated_data.pop("created_date", None)
    #     validated_data.pop("unique_key", None)
    #     mileage = Mileage.objects.create(**validated_data)
    #     return mileage

    # def update(self, instance, validated_data):
    #     validated_data.pop("created_date", None)
    #     validated_data.pop("unique_key", None)
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance
