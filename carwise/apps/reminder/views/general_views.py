# Standard Library
from apps.common.message import AppMessages
from datetime import datetime, timedelta

# First Party Imports
from apps.reminder.helper_functions import check_custom_fields, check_original_fields
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


# ______________________ car company List API ______________________ #


@extend_schema(tags=["general"])
class CarListAPI(ListAPIView):
    """Get  car list"""

    permission_classes = [IsAuthenticated]
    serializer_class = CarCompanyListSerializer

    def get_queryset(self):
        return CarCompany.objects.all()


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
                pct = 100 * distance_traveled / total_distance
                item_dict = {
                    "name": Mileage._meta.get_field(field).verbose_name,
                    "amount": last_changed,
                    "limit": future_change,
                    "pct": AppMessages.OVERDUE.value if pct > 100 else round(pct, 2),
                }
                response_list.append(item_dict)
        return response_list

    def get_custom_fields(self, car, mileage):
        fields = car.car_custom_fileds.all()
        response_list = []
        for field in fields:
            resp_dict = {}
            if field.last_mileage_changed and field.mileage_per_change:

                amount = field.last_mileage_changed
                limit = field.mileage_per_change + field.last_mileage_changed
                diff = mileage.mileage - field.last_mileage_changed
                pct = 100 * diff / field.mileage_per_change
                resp_dict = {
                    "amount": amount,
                    "limit": limit,
                    "pct": AppMessages.OVERDUE.value if pct > 100 else round(pct, 2),
                }

            if field.last_date_changed:
                # Check if month_per_changes is not None
                expected_date = field.last_date_changed + timedelta(
                    days=30 * field.month_per_changes
                )
                current_date = datetime.now()
                # Calculate the difference
                date_difference = expected_date - current_date.date()
                # Calculate the total time period in days
                total_period_days = (expected_date - field.last_date_changed).days

                # Calculate the elapsed time in days
                elapsed_days = (current_date.date() - field.last_date_changed).days

                # Calculate the percentage of time elapsed
                percentage_elapsed = (elapsed_days / total_period_days) * 100
                resp_dict["date_pct"] = (
                    AppMessages.OVERDUE.value
                    if percentage_elapsed > 100
                    else round(percentage_elapsed, 2)
                )
                date_limit = (
                    AppMessages.OVERDUE.value
                    if date_difference < timedelta(0)
                    else date_difference
                )
                #
                years, months, days = timedelta_to_years_months_days(
                    abs(date_difference)
                )
                parts = []
                if years != 0:
                    parts.append(AppMessages.YEAR.value.format(years))
                if months != 0:
                    parts.append(AppMessages.MONTH.value.format(months))
                if days != 0:
                    parts.append(AppMessages.DAY.value.format(days))

                if len(parts) > 1:
                    message = f" {AppMessages.AND.value} ".join(
                        f"{AppMessages.COMMA.value} ".join(parts).rsplit(
                            f"{AppMessages.COMMA.value} ", 1
                        )
                    )
                elif len(parts) == 1:
                    message = parts[0]

                elif len(parts) == 0:
                    # if exact date has come
                    message = AppMessages.DAY.value.format("1")

                if date_difference <= timedelta(0):
                    date_limit = AppMessages.DATE_PASSED.value.format(message)
                else:
                    date_limit = AppMessages.DATE_FUTURE.value.format(message)

                resp_dict["date"] = field.last_date_changed
                resp_dict["date_limit"] = date_limit

            if resp_dict:  # if the dict was not empty
                resp_dict["name"] = field.name
                response_list.append(resp_dict)
        return response_list

    def get(self, request, *args, **kwargs):
        car = self.get_object()
        car_setup = car.setup
        mileages = Mileage.objects.filter(car=car).order_by("-created_date")
        response_dict = {}
        if mileages:
            last_mileage = mileages.first()
            orginal_resp_list = self.get_original_fields(car_setup, last_mileage)
            custom_resp_list = self.get_custom_fields(car, last_mileage)
            if orginal_resp_list is None:
                orginal_resp_list = []
            if custom_resp_list is None:
                custom_resp_list = []
            response_dict["mileage"] = last_mileage.mileage

        # for field in
        response_dict["statistic"] = orginal_resp_list + custom_resp_list
        return Response(response_dict, status.HTTP_200_OK)

    def get_object(self):
        return get_object_or_404(
            Car, unique_key=self.kwargs["unique_key"], user=self.request.user
        )


# ______________________ Get Notifications for Users ______________________ #


def get_notification_for_user(user):
    """
    Get notifications for a given user based on car mileages and custom fields.
    """
    message_dict = {}
    message_parts = []
    user_cars = user.user_cars.all()

    if user_cars:
        for car in user_cars:
            mileages = Mileage.objects.filter(car=car).order_by("-created_date")
            if mileages.exists():
                last_mileage = mileages.first().mileage
                last_mileage_obj = mileages.first()

                # Check custom fields and original fields
                check_custom_fields(car, last_mileage, message_dict)
                check_original_fields(car, last_mileage_obj, last_mileage, message_dict)

        for car_key, fields in message_dict.items():
            car_name = Car.objects.get(unique_key=car_key).name
            count = len(fields)
            if count > 0:
                message_parts.append(
                    f"{car_name} has {count} elements"
                )  # Join the message parts to form the final string
        if message_parts:
            result_message = (
                ", ".join(message_parts[:-1])
                + f" and {message_parts[-1]} to check based on estimated mileage."
            )
        else:
            result_message ="checked. There is nothing to update."

    return result_message

# ______________________ Data Checker ______________________ #

@extend_schema(tags=["checker"])
class DataChecker(APIView):
    """checks the dates and mileage for all cars blong to a user"""
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_dict = {}

    def get_queryset(self):
        user = self.request.user
        return user.user_cars.all()

    def get(self, request):
        user_cars = self.get_queryset()

        if user_cars:
            for car in user_cars:
                mileages = Mileage.objects.filter(car=car).order_by("-created_date")
                if mileages.exists():
                    last_mileage = mileages.first().mileage
                    last_mileage_obj = mileages.first()

                    # Check custom fields and original fields
                    check_custom_fields(car, last_mileage, self.message_dict)
                    check_original_fields(
                        car, last_mileage_obj, last_mileage, self.message_dict
                    )

        return Response(self.message_dict, status=status.HTTP_200_OK)
