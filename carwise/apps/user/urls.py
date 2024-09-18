from django.urls import path

from apps.user.views import (
    ForgotPasswordView,
    LogoutAPI,
    RegisterAPIView,
    RetrieveUpdateUserView,
    ChangePasswordView,
    FCMTokenViewSet,
    VerifyCodeView,
    ResetPasswordAPI,
)

urlpatterns = [
    path("logout/", LogoutAPI.as_view(), name="token_obtain_pair"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("profile/", RetrieveUpdateUserView.as_view(), name="register"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("varify-code/", VerifyCodeView.as_view(), name="change-password"),
    path("reset-password/", ResetPasswordAPI.as_view(), name="reset_password"),
    path("fcm-token/", FCMTokenViewSet.as_view(), name="fcm_token"),
]
