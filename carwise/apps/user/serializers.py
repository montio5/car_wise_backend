import random
from django.conf import settings
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
from apps.common.message import AppMessages
from django.core.mail import EmailMessage

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
        # Check if the email exists in the database
        users_email = User.objects.filter(email__iexact=value.strip())
        if not users_email.exists():
            raise serializers.ValidationError(AppMessages.USER_NOT_FOUND_MSG.value)
        return users_email.first()

    def send_password_reset_email(self):
        # Retrieve the validated email
        email_user = self.validated_data["email"]

        # Expire any existing requests
        PasswordResetRequest.objects.filter(user=email_user, is_expired=False).update(
            is_expired=True
        )
        # Generate a random reset code
        code = random.randint(100000, 999999)
        # Create a new password reset request
        PasswordResetRequest.objects.create(user=email_user, code=str(code))

        # Prepare the email subject and message
        subject = AppMessages.FORGOT_PASSWORD.value
        message = """
        <div style="text-align: center;">
            <p>{}</p>
            <p><strong style="font-size: 18px;">{}</strong></p>
            <p>{}</p>
        </div>
        """.format(
            AppMessages.YOUR_RESET_PASSWORD.value,
            code,
            AppMessages.USE_CODE_FOR_REST_PASS.value,
        )

        # Create the email message
        email_message = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[email_user.email],
        )

        # Ensure the email is sent as HTML
        email_message.content_subtype = "html"
        email_message.send(fail_silently=False)


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
