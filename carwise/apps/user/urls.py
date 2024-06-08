from django.urls import path

from apps.user.views import LogoutAPI, RegisterAPIView , RetrieveUpdateUserView, ChangePasswordView

urlpatterns = [
    path("logout/", LogoutAPI.as_view(), name="token_obtain_pair"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("profile/", RetrieveUpdateUserView.as_view(), name="register"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),

]
