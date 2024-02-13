# Third Party Packages
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.common.message import AppMessages

from apps.reminder.models import Car, CarCustomSetup, CustomFiled

# __________________  custom_field Serializer ___________________ #


class CustomFieldSerializer(serializers.ModelSerializer):
    """serializer for getting, updating custom_field detail"""

    # car = serializers.PrimaryKeyRelatedField(
    #     queryset=Car.objects.all(),
    # )

    class Meta:
        model = CustomFiled
        fields = "__all__"

    def validate(self, object):
        mileage_per_change = object.get("mileage_per_change", None)
        year_per_changes = object.get("year_per_changes", None)
        month_per_changes = object.get("month_per_changes", None)
        if (
            mileage_per_change is None
            and year_per_changes is None
            and month_per_changes is None
        ):
            raise ValidationError(AppMessages.INVALID_CUSTOM_FIELD.value)
        return object

    def create(self, validated_data):
        custom_field = CustomFiled.objects.create(**validated_data)
        return custom_field

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# __________________   Car Custom Setup Serializer ___________________ #


class CustomSetupSerializer(serializers.ModelSerializer):
    """serializer for getting, updating custom_field detail"""

    car = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(),
        required=True,
    )
    custom_fields = CustomFieldSerializer(many=True, read_only=True)

    class Meta:
        model = CarCustomSetup
        fields = ["__all__", "custom_fields"]
