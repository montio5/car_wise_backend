from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from apps.common.message import AppMessages
from apps.user.models import PasswordResetRequest
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

class UserSerializer(serializers.ModelSerializer):

    def validate_email(self, value):
        try:
            EmailValidator()(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format.")

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
    email = serializers.CharField(required=True)

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
            raise serializers.ValidationError(AppMessages.PASSWORD_DO_NOT_MATCH.value)
        return data

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                AppMessages.CURRENT_PASSWORD_IS_INCORRECT.value
            )
        return value


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(AppMessages.USER_NOT_FOUND_MSG.value)
        return value


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=10, required=True)

    def validate_code(self, value):
        # Filter PasswordResetRequest by code and validity
        reset_request = (
            PasswordResetRequest.objects.filter(code=value, is_valid=False)
            .order_by("-created_at")
            .first()
        )

        if not reset_request:
            raise serializers.ValidationError(
                AppMessages.RESET_CODE_NOT_FOUND_MSG.value
            )

        if reset_request.is_expired == True:
            raise serializers.ValidationError(AppMessages.RESET_CODE_EXPIRED_MSG.value)

        # Check if the code is expired
        expiration_time = reset_request.created_at + timedelta(minutes=5)
        if timezone.now() > expiration_time:
            reset_request.is_expired = True
            reset_request.save()
            raise serializers.ValidationError(AppMessages.RESET_CODE_EXPIRED_MSG.value)
        return reset_request


class ResetPasswordSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=10, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate_code(self, value):
        reset_request = (
            PasswordResetRequest.objects.filter(code=value, is_valid=True)
            .order_by("-created_at")
            .first()
        )
        if not reset_request or reset_request is None:
            raise serializers.ValidationError(
                AppMessages.RESET_CODE_NOT_FOUND_MSG.value
            )

        if reset_request.is_expired:
            raise serializers.ValidationError(AppMessages.RESET_CODE_EXPIRED_MSG.value)

        expiration_time = reset_request.created_at + timedelta(minutes=5)
        if timezone.now() > expiration_time:
            reset_request.is_expired = True
            reset_request.save()
            raise serializers.ValidationError(AppMessages.RESET_CODE_EXPIRED_MSG.value)

        return reset_request

    def validate(self, data):
        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError(AppMessages.PASSWORD_DO_NOT_MATCH.value)
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):

        try:
            # Case-insensitive email lookup
            user = User.objects.get(email__iexact=attrs["username"])
        except User.DoesNotExist:
            raise AuthenticationFailed(
               AppMessages.USER_NOT_FOUND_MSG
            )
        attrs["username"] = user.email
        # Validate with parent method after adjusting the username
        return super().validate(attrs)
