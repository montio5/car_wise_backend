from django.contrib.auth.models import User
from rest_framework import serializers

from apps.common.message import AppMessages


class UserSerializer(serializers.ModelSerializer):

    def validate_email(self, value):
        request = self.context.get("request")
        if request.method == "PUT":
            instance = self.instance
            user_with_entered_email = User.objects.filter(email__iexact=value).exclude(
                id=instance.id
            )
        else:
            user_with_entered_email = User.objects.filter(email__iexact=value)

        if user_with_entered_email:
            raise serializers.ValidationError(AppMessages.USER_EXISTS.value)
        return value

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]


class RegisterUserSerializer(UserSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["email"], **validated_data
        )
        return user

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ["password"]


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError("New passwords do not match.")
        return data

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                AppMessages.CURRENT_PASSWORD_IS_INCORRECT.value
            )
        return value
