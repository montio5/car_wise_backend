from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
)
from apps.user.models import BlacklistedToken, UserFCMToken
from apps.user.serializers import UserSerializer,RegisterUserSerializer,ChangePasswordSerializer
from django.core.mail import send_mail
from django.contrib.auth.models import User
import random
from django.conf import settings
from rest_framework import status


class RegisterAPIView(CreateAPIView):

    permission_classes = []
    serializer_class = RegisterUserSerializer


class SignInAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
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
        serializer =  ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'detail': 'Password updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return Response({"detail": "Authorization header missing."}, status=status.HTTP_400_BAD_REQUEST)

            token = auth_header.split(' ')[1]
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
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            code  = random.randint(100000, 999999)

            send_mail(
                "Forgot Password",
                f"Your reset code is: {code}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            # Store the code in the user's session or a cache
            request.session["reset_code"] = code
            return Response(
                {"message": "Code sent to your email"}, status=status.HTTP_200_OK
            )
        return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    def post(self, request):
        code = request.data.get("code")
        stored_code = request.session.get("reset_code")
        if code == stored_code:
            return Response(
                {"message": "Password reset enabled"}, status_code=status.HTTP_200_OK
            )
        return Response({"error": "Invalid code"}, status_code=400)
