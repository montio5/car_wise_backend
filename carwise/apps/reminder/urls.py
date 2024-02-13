from django.urls import include, path

from apps.reminder.views.car_views import (
    CarAddAPI,
    CarUpdateDestroyAPI,
    MileageAddAPI,
    MileageUpdateAPI,
    UserCarListAPI,
)
from apps.reminder.views.custom_views import (
    CarCustomSetupUpdateDestroyAPI,
    CustomFieldAddAPI,
    CustomFieldListAPI,
    CustomFieldUpdateDestroyAPI,
)

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
# _________________________ mileage ________________________ #

mileage = [
    path("new/", MileageAddAPI.as_view(), name="add_mileage"),
    path(
        "<str:unique_key>/",
        MileageUpdateAPI.as_view(),
        name="mileage_edit_delete",
    ),
]
# _________________________ custom field ________________________ #

custom_field = [
    path("", CustomFieldListAPI.as_view(), name="car_custom_fields_list"),
    path("new/", CustomFieldAddAPI.as_view(), name="add_car"),
    path(
        "<int:id>/",
        CustomFieldUpdateDestroyAPI.as_view(),
        name="car_edit_delete",
    ),
]
# _________________________ car custom setup ________________________ #

car_custom_setup = [
    path(
        "<str:car_unique_key>/",
        CarCustomSetupUpdateDestroyAPI.as_view(),
        name="car_setup_edit_delete",
    ),
]
# _________________________________________________ #

urlpatterns = [
    path("user-cars/", include(car)),
    path("mileage/", include(mileage)),
    path("custom-field/<str:car_unique_key>/", include(custom_field)),
    path("custom-setup/", include(car_custom_setup)),
]
