from django.urls import include, path

from apps.reminder.views.car_views import CarAddAPI, CarUpdateDestroyAPI, UserCarListAPI

# _________________________ car ________________________ #

car = [
    path("", UserCarListAPI.as_view(), name="car_list"),
    path("new/", CarAddAPI.as_view(), name="add_car"),
    path(
        "<str:unique_key>/",
        CarUpdateDestroyAPI.as_view(),
        name="car_edit_delete",
    ),
]
# _________________________________________________ #

urlpatterns = [
    path("user-cars/", include(car)),
]
