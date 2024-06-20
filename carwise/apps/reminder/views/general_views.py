# Standard Library
from apps.common.message import AppMessages
from datetime import datetime, timedelta
from django.utils import timezone

# First Party Imports
from apps.reminder.models import Car, CarCompany, Mileage
from apps.common.functions import timedelta_to_years_months_days
from rest_framework.views import APIView
from apps.reminder.serializers.general_serializers import CarCompanyListSerializer

# Third Party Packages
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

# Third Party Packages
from rest_framework.generics import (
    ListAPIView,
    get_object_or_404,
)

SERIOUS = "Serious"
MEDIUM = "Medium"
INFO = "Informational"
CUSTOM = "Custom"


# ______________________ Get Car Dashboard API ______________________ #


@extend_schema(tags=["general"])
class CarِDashboardAPI(APIView):
    """Get car dashboard detail"""

    permission_classes = [IsAuthenticated]

    def get_original_fields(self, car_setup, mileage):
        exclude_fields = [
            "_state",
            "id",
            "car_id",
            "mileage",
            "created_date",
            "unique_key",
        ]
        filled_fields = [
            key
            for key in mileage.__dict__.keys()
            if mileage.__dict__[key] is not None and key not in exclude_fields
        ]
        response_list = []
        for field in filled_fields:
            if hasattr(mileage, field):
                last_changed = getattr(mileage, field)
                future_change = getattr(car_setup, field) + last_changed
                # Calculate total distance between changes
                total_distance = getattr(car_setup, field)

                # Calculate distance traveled since the last change
                distance_traveled = mileage.mileage - last_changed
                pct = 100 * distance_traveled/ total_distance
                item_dict = {
                    "name":Mileage._meta.get_field(field).verbose_name ,
                    "amount": last_changed,
                    "limit": future_change,
                    "pct": "overdue" if pct >100 else round(pct, 2),
                }
                response_list.append(item_dict)
        return response_list

    def get_custom_fields(self, car, mileage):
        # breakpoint()
        fields = car.car_custom_fileds.all()
        response_list = []

        for field in fields:
            resp_dict = {}
            if field.last_mileage_changed:
                amount = field.last_mileage_changed
                limit = field.mileage_per_change + field.last_mileage_changed
                pct = 100 * mileage.mileage/limit
                resp_dict = {"amount": amount, "limit": limit, "pct":"overdue" if pct >100 else round(pct, 2)}
            if field.last_date_changed:
                    # Check if month_per_changes is not None
                    expected_date = field.last_date_changed + timedelta(days=30 * field.month_per_changes)
                    current_date = datetime.now()
                    # Calculate the difference
                    date_difference = expected_date - current_date.date()
                    # Calculate the total time period in days
                    total_period_days = (expected_date - field.last_date_changed).days

                    # Calculate the elapsed time in days
                    elapsed_days = (current_date.date() - field.last_date_changed).days

                    # Calculate the percentage of time elapsed
                    percentage_elapsed = (elapsed_days / total_period_days) * 100
                    resp_dict["date_pct"] = "overdue" if percentage_elapsed > 100 else round(percentage_elapsed, 2) 
                    date_limit = "overdue" if date_difference < timedelta(0) else date_difference  
                    #
                    years, months, days =timedelta_to_years_months_days(abs(date_difference))
                    message =""
                    if years!=0:
                       message += AppMessages.YEAR.value.format(years)
                    if months!=0:
                        message += AppMessages.MONTH.value.format(months)
                    if days!=0:
                       message += AppMessages.DAY.value.format(days)
                    if date_difference< timedelta(0):
                        date_limit = AppMessages.DATE_PASSED.value.format(message)
                    else:
                        date_limit = AppMessages.DATE_FUTURE.value.format(message)

                
                    resp_dict["date"] = field.last_date_changed
                    resp_dict["date_limit"] = date_limit

            if len(resp_dict)>0:
                resp_dict["name"]=field.name 
                response_list.append(resp_dict)
        return response_list

    def get(self, request, *args, **kwargs):
        car = self.get_object()
        car_setup = car.setup
        mileages = Mileage.objects.filter(car=car).order_by("-created_date")
        response_dict ={}
        if mileages:
            last_mileage = mileages.first()
            orginal_resp_list =self.get_original_fields(car_setup, last_mileage)
            custom_resp_list= self.get_custom_fields(car, last_mileage)
            if orginal_resp_list is None:
                orginal_resp_list=[]
            if custom_resp_list is None:
                custom_resp_list=[]
            response_dict["mileage"] = last_mileage.mileage

        # for field in
        response_dict['statistic'] =orginal_resp_list+custom_resp_list
        return Response(response_dict, status.HTTP_200_OK)

    def get_object(self):
        return get_object_or_404(
            Car, unique_key=self.kwargs["unique_key"], user=self.request.user
        )


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
            if (
                field.mileage_per_change is not None
                or field.month_per_changes is not None
            ):
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
            if mileage.mileage > (
                field.mileage_per_change + field.last_mileage_changed
            ):
                self.message_dict[car.unique_key][field.id] = {
                    "status": CUSTOM,
                    "field_name": field.name,
                    "message": AppMessages.CHECK_FIELD_MILEAGE.value.format(field.name),
                    "car": car.name,
                }
        except TypeError:
            pass

    def check_date_condition(self, car, field):
        try:
            expected_date = field.last_date_changed + timedelta(
                days=30 * field.month_per_changes
            )
            if expected_date < timezone.now().date():
                self.message_dict[car.unique_key][field.id] = {
                    "status": CUSTOM,
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
