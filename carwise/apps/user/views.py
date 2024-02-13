from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import (
    CreateAPIView,
)
from apps.user.serializers import UserSerializer


class RegisterAPIView(CreateAPIView):

    permission_classes = []
    serializer_class = UserSerializer


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


class LogOutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(
                    {"success": "User logged out successfully"},
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {"error": "Invalid refresh token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Refresh token not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
