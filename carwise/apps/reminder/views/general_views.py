# Standard Library
from apps.common.message import AppMessages
from datetime import timedelta
from django.utils import timezone

# First Party Imports
from apps.reminder.models import CarCompany, Mileage
from rest_framework.views import APIView
from apps.reminder.serializers.general_serializers import CarCompanyListSerializer

# Third Party Packages
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView

SERIOUS = "Serious"
MEDIUM = "Medium"
INFO = "Informational"
CUSTOM = "CUSTOM"

# ______________________ car company List API ______________________ #


@extend_schema(tags=["general"])
class CarListAPI(ListAPIView):
    """Get  car list"""

    permission_classes = [IsAuthenticated]
    serializer_class = CarCompanyListSerializer

    def get_queryset(self):
        return CarCompany.objects.all()


# ______________________ Data Checker API ______________________ #


@extend_schema(tags=["checker"])
class DataChecker(APIView):
    permission_classes = [IsAuthenticated]
    message_dict = {}

    def get(self, request):
        user = self.request.user
        user_cars = user.user_cars.all()
        if user_cars:
            for car in user_cars:
                mileages = Mileage.objects.filter(car=car).order_by("-created_date")
                if mileages:
                    last_mileage = mileages.first()
                    self.custom_field_check(car, last_mileage)
                    self.original_fields_check(car, last_mileage)
            return Response(self.message_dict, status.HTTP_200_OK)
    
    def custom_field_check(self, car, mileage):
        custom_fields = car.car_custom_fileds.all()
        for field in custom_fields:
            if field.mileage_per_change is not None or field.month_per_changes is not None:
                car_key = car.unique_key
                if car_key not in self.message_dict:
                    self.message_dict[car_key] = {field.id: {}}
                if field.id not in self.message_dict[car_key]:
                    self.message_dict[car_key][field.id] = {}

                # Check mileage condition
                self.check_mileage_condition(car, field, mileage)

                # Check date condition
                self.check_date_condition(car, field)

    def check_mileage_condition(self, car, field, mileage):
        try:
            if mileage.mileage > (field.mileage_per_change + field.last_mileage_changed):
                self.message_dict[car.unique_key][field.id]= {
                    "status": "CUSTOM",
                    "field_name": field.name,
                    "message": AppMessages.CHECK_FIELD_MILEAGE.value.format(field.name),
                    "car": car.name,
                }
        except TypeError:
            pass

    def check_date_condition(self, car, field):
        try:
            expected_date = field.last_date_changed + timedelta(days=30 * field.month_per_changes)
            if expected_date < timezone.now().date():
                self.message_dict[car.unique_key][field.id]= {
                    "status": "CUSTOM",
                    "field_name": field.name,
                    "message": AppMessages.CHECKER_FIELD_DATE.value.format(field.name),
                    "car": car.name,
                }
        except TypeError:
            pass



    def original_fields_check(self, car, mileage):
        field_details = {
            "engine_oil": {"status": SERIOUS},
            "gearbox_oil": {"status": MEDIUM},
            "hydraulic_fluid": {"status": INFO},
            "oil_filter": {"status": SERIOUS},
            "fuel_filter": {"status": MEDIUM},
            "air_filter": {"status": MEDIUM},
            "cabin_air_filter": {"status": INFO},
            "timing_belt": {"status": SERIOUS},
            "timing_belt_last_updated_date": {"status": SERIOUS},
            "alternator_belt": {"status": MEDIUM},
            "rear_brake_pads": {"status": INFO},
            "front_brake_pads": {"status": INFO},
            "spark_plug": {"status": SERIOUS},
            "front_suspension": {"status": INFO},
            "clutch_plate": {"status": MEDIUM},
        }
        if car.unique_key not in self.message_dict:
            self.message_dict[car.unique_key] = {}
        car_setup_data = car.setup
        for field_name, details in field_details.items():
            field_value = getattr(mileage, field_name)
            if field_name == "timing_belt_last_updated_date":
                if (
                    field_value is not None
                    and field_value
                    + timedelta(
                        days=365 * getattr(car_setup_data, "timing_belt_max_year")
                    )
                    < timezone.now()
                ):
                    self.message_dict[car.unique_key]["timing_belt"]["date"] = {
                        "status": details["status"],
                        "field_name": Mileage._meta.get_field(field_name).verbose_name,
                        "message": AppMessages.CHECK_FIELD_MILEAGE.value.format(
                            Mileage._meta.get_field(field_name).verbose_name
                        ),
                        "car": car.name,
                    }
            else:
                setup_data = getattr(car_setup_data, field_name)
                if (
                    field_value is not None
                    and field_value + setup_data < mileage.mileage
                ):
                    self.message_dict[car.unique_key][field_name] = {
                        "status": details["status"],
                        "field_name": Mileage._meta.get_field(field_name).verbose_name,
                        "message": AppMessages.CHECK_FIELD_MILEAGE.value.format(
                            Mileage._meta.get_field(field_name).verbose_name
                        ),
                        "car": car.name,
                    }
