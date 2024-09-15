from django.urls import include, path

from apps.reminder.views.car_views import (
    CarAddAPI,
    CarUpdateDestroyAPI,
    MileageView,
    UserCarListAPI,
)
from apps.reminder.views.custom_views import (
    CarCustomSetupUpdateDestroyAPI,
    CustomFieldAddAPI,
    CustomFieldListAPI,
    CustomFieldUpdateDestroyAPI,
)
from apps.reminder.views.general_views import CarListAPI, DataChecker,CarِDashboardAPI


# _________________________ general ________________________ #

general_apis = [
    path("car-models", CarListAPI.as_view(), name="car_models"),
    path("car-dashboard/<str:unique_key>/", CarِDashboardAPI.as_view(), name="car_dashboard"),
    # path("notification", GetNotificationAPI.as_view(), name="notification"),
]
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
    path(
        "<str:unique_key>/",
        MileageView.as_view(),
        name="add_edit_get_mileage",
    ),
]
# _________________________ custom field ________________________ #

custom_field = [
    path("", CustomFieldListAPI.as_view(), name="custom_fields_list"),
    path("new/", CustomFieldAddAPI.as_view(), name="add_custom_field"),
    path(
        "<int:id>/",
        CustomFieldUpdateDestroyAPI.as_view(),
        name="custom_field_edit_delete",
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
# _________________________ general apis ________________________ #

check_data = [
    path(
        "",
        DataChecker.as_view(),
        name="check_data",
    ),
]

# _________________________________________________ #

urlpatterns = [
    path("user-cars/", include(car)),
    path("mileage/", include(mileage)),
    path("custom-field/<str:car_unique_key>/", include(custom_field)),
    path("custom-setup/", include(car_custom_setup)),
    path("check-data/", include(check_data)),
    path("", include(general_apis)),
]
