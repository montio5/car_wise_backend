from django.urls import path

from apps.user.views import LogOutAPIView, RegisterAPIView

urlpatterns = [
    path("logout/", LogOutAPIView.as_view(), name="token_obtain_pair"),
    path("register/", RegisterAPIView.as_view(), name="register"),
]
