from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
)
from apps.user.models import BlacklistedToken, PasswordResetRequest, UserFCMToken
from apps.user.serializers import (
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    UserSerializer,
    RegisterUserSerializer,
    ChangePasswordSerializer,
    VerifyCodeSerializer,
)
from django.core.mail import send_mail
from django.contrib.auth.models import User
import random
from django.conf import settings
from rest_framework import status
from apps.common.message import AppMessages
from django.utils.html import format_html
from django.core.mail import EmailMessage


class RegisterAPIView(CreateAPIView):

    permission_classes = []
    serializer_class = RegisterUserSerializer


class SignInAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Use iexact to find the user regardless of username case
        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return Response(
                {"error": AppMessages.USER_NOT_FOUND_MSG.value}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Authenticate using the retrieved user and provided password
        user = authenticate(username=user.email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class RetrieveUpdateUserView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    http_method_names = ["put", "get"]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data["new_password"])
            request.user.save()
            return Response(
                {"detail": "Password updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return Response(
                    {"detail": "Authorization header missing."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = auth_header.split(" ")[1]
            BlacklistedToken.objects.create(token=token)

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FCMTokenViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get("fcm_token")
        if token:
            UserFCMToken.objects.filter(token=token).delete()

            # Save or update the FCM token associated with the user
            UserFCMToken.objects.update_or_create(
                user=request.user,
                defaults={"token": token},
            )
            return Response({"message": "FCM token saved successfully."})
        return Response({"error": "No token provided."}, status=400)


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.get(email__iexact=email)
        code = random.randint(100000, 999999)

        # Expire any existing requests
        PasswordResetRequest.objects.filter(user=user, is_expired=False).update(
            is_expired=True
        )

        # Create new PasswordResetRequest
        PasswordResetRequest.objects.create(user=user, code=str(code))

        # Send the email
        subject = AppMessages.FORGOT_PASSWORD.value
        # Format the HTML content
        message = """
        <div style="text-align: center;">
            <p>{}</p>
            <p><strong style="font-size: 18px;">{}</strong></p>
            <p>{}</p>
        </div>
        """.format(
            AppMessages.YOUR_RESET_PASSWORD.value, 
            code, 
            AppMessages.USE_CODE_FOR_REST_PASS.value
        )

        # Create the EmailMessage object
        email_message = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
        )
        email_message.content_subtype = "html"  # This makes sure the email is sent as HTML
        email_message.send(fail_silently=False)

        return Response(
            {"message": AppMessages.RESET_CODE_SENT_MSG.value},
            status=status.HTTP_200_OK,
        )


class VerifyCodeView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_request = serializer.validated_data["code"]
        reset_request.is_valid = True
        reset_request.save()

        return Response(
            {"message": AppMessages.PASSWORD_RESET_ENABLED_MSG.value},
            status=status.HTTP_200_OK,
        )


class ResetPasswordAPI(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_req_obj = serializer.validated_data["code"]
        new_password = serializer.validated_data["new_password"]
        user_object = PasswordResetRequest.objects.get(code=reset_req_obj.code).user
        # Update the user's password
        user_object.set_password(new_password)
        user_object.save()

        # Mark the reset request as expired
        reset_req_obj.is_expired = True
        reset_req_obj.save()

        return Response(
            {"detail": AppMessages.PASSWORD_UPDATED_SUCCESS_MSG.value}, status=status.HTTP_200_OK
        )
