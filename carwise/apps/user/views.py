from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
)
from apps.user.models import BlacklistedToken, PasswordResetRequest, UserFCMToken
from apps.user.serializers import (
    CustomTokenObtainPairSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    UserSerializer,
    RegisterUserSerializer,
    ChangePasswordSerializer,
    VerifyCodeSerializer,
)
from rest_framework import status
from apps.common.message import AppMessages
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterAPIView(CreateAPIView):

    permission_classes = []
    serializer_class = RegisterUserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


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

        # Call the custom method in the serializer to handle code generation and email sending
        serializer.send_password_reset_email()

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
