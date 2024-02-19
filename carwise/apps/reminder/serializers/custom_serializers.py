# Third Party Packages
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.common.message import AppMessages

from apps.reminder.models import Car, CarCustomSetup, CustomFiled

# __________________  custom_field Serializer ___________________ #


class CustomFieldSerializer(serializers.ModelSerializer):
    """serializer for getting, updating custom_field detail"""

    class Meta:
        model = CustomFiled
        fields = [
            "id",
            "name",
            "mileage_per_change",
            "month_per_changes",
            "last_mileage_changed",
            "last_date_changed",
        ]

    def validate(self, validated_data):
        mileage_per_change = validated_data.get("mileage_per_change", None)
        month_per_changes = validated_data.get("month_per_changes", None)
        if mileage_per_change is None and month_per_changes is None:
            raise ValidationError(
                AppMessages.INVALID_CUSTOM_FIELD.value.format(
                    "mileage_per_change, month_per_changes"
                )
            )

        #
        last_mileage_changed = validated_data.get("last_mileage_changed", None)
        last_date_changed = validated_data.get("last_date_changed", None)
        if mileage_per_change is not None:
            if last_mileage_changed is None:
                raise ValidationError(
                    AppMessages.MUST_FIELD.value.format("last_mileage_changed")
                )
        if month_per_changes is not None:
            if last_date_changed is None:
                raise ValidationError(
                    AppMessages.MUST_FIELD.value.format("last_date_changed")
                )
        return validated_data

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
