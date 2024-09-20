# Standard Library
from apps.common.message import AppMessages
from datetime import timedelta
from django.utils import timezone

from apps.reminder.models import Mileage

SERIOUS = "Serious"
MEDIUM = "Medium"
INFO = "Informational"
CUSTOM = "Custom"

# ______________________ Helper Functions ______________________ #


def check_condition(condition, message_dict, car, field, field_id, status, message):
    """
    Reusable function to check a condition and update message dict.
    """
    if condition:
        if car.unique_key not in message_dict:
            message_dict[car.unique_key] = {}
        if field_id : # is custom_field
            if field_id not in message_dict[car.unique_key]:
                message_dict[car.unique_key][field_id]={}
            message_dict[car.unique_key][field_id] = {
                "status": status,
                "field_name": field.name,
                "message": message.format(field.name),
                "car": car.name,
            }
        else:
            field_name = Mileage._meta.get_field(field).verbose_name
            message_dict[car.unique_key][field] = {
                "status": status,
                "field_name": field_name,
                "message": message.format(field_name),
                "car": car.name,
            }


def check_mileage_condition(car, field, mileage, message_dict):
    """
    Check mileage condition and update message dict.
    """
    try:
        condition = mileage > (field.mileage_per_change + field.last_mileage_changed)
        message = AppMessages.CHECK_FIELD_MILEAGE.value
        check_condition(condition, message_dict, car, field, field.id, CUSTOM, message)
    except TypeError:
        pass


def check_date_condition(car, field, message_dict):
    """
    Check date condition and update message dict.
    """
    try:
        expected_date = field.last_date_changed + timedelta(
            days=30 * field.month_per_changes
        )
        condition = expected_date < timezone.now().date()
        message = AppMessages.CHECKER_FIELD_DATE.value
        check_condition(condition, message_dict, car, field, field.id, CUSTOM, message)
    except TypeError:
        pass


def check_custom_fields(car, mileage, message_dict):
    """
    Check custom fields (both mileage and date conditions) for a car.
    """
    custom_fields = car.car_custom_fileds.all()
    for field in custom_fields:
        if field.mileage_per_change is not None or field.month_per_changes is not None:
            check_mileage_condition(car, field, mileage, message_dict)
            check_date_condition(car, field, message_dict)


def check_original_fields(car, mileage_obj, mileage, message_dict):
    """
    Check original fields like engine_oil, gearbox_oil, etc. for a car.
    """
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

    car_setup_data = car.setup
    for field_name, details in field_details.items():
        field_value = getattr(mileage_obj, field_name)

        # Special case for timing belt last updated date
        if field_name == "timing_belt_last_updated_date":
            if field_value is not None:
                condition = (
                    field_value
                    + timedelta(
                        days=365 * getattr(car_setup_data, "timing_belt_max_year")
                    )
                    < timezone.now()
                )
                message = AppMessages.CHECK_FIELD_MILEAGE.value
                check_condition(
                    condition,
                    message_dict,
                    car,
                    field_value,
                    "timing_belt",
                    details["status"],
                    message,
                )
        else:
            setup_data = getattr(car_setup_data, field_name)
            if field_value is not None and field_value + setup_data <= mileage:
                message = AppMessages.CHECK_FIELD_MILEAGE.value
                check_condition(
                    True,
                    message_dict,
                    car,
                    field_name,
                    None,
                    details["status"],
                    message,
                )
