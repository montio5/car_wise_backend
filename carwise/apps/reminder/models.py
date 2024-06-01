from django.db import models
from django.contrib.auth.models import User
import functools
import secrets
from django.utils.translation import gettext_lazy as _


YEARLY_MIALAGE = 50000
ENGINE_OIL = 6000
GEARBOX_OIL = 70000
BRAKE_FLUID = YEARLY_MIALAGE
HYDRAULIC_FLUID = YEARLY_MIALAGE
#
OIL_FILTER = 6000
FUEL_FILTER = 12000
AIR_FILTER = YEARLY_MIALAGE
CABIN_AIR_FILTER = YEARLY_MIALAGE
#
TIMING_BELT = 60000
TIMING_BELT_MAX_YEAR = 5
ALTERNATOR_BELT = 30000
FRONT_BRAKE_PAD = 25000
REAR_BRAKE_PAD = 70000
SPARK_PLUG = 60000
FRONT_SUSPENSION = 80000
CLUTCH_PLATE = 60000
#
COOLER_GAS_CHANGE_YEARS = 3  # every 3 years
HYDRAULIC_FLUID_CHANGE_YEARS = 1
CABIN_AIR_FILTER_CHANGE_YEARS = 1


# COOLER_GAS
# --------------------------------------
class Car(models.Model):
    unique_key = models.CharField(
        unique=True,
        default=functools.partial(secrets.token_urlsafe, nbytes=32),
        max_length=70,
    )
    name = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_cars")
    car_model = models.ForeignKey(
        "CarModel", on_delete=models.CASCADE, related_name="model_cars"
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.unique_key + "-" + self.name + "user :" + str(self.user.id)


# --------------------------------------


class Mileage(models.Model):
    car = models.ForeignKey(
        "Car", on_delete=models.CASCADE, related_name="car_mileages"
    )
    mileage = models.PositiveBigIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    unique_key = models.CharField(
        unique=True,
        default=functools.partial(secrets.token_urlsafe, nbytes=32),
        max_length=70,
    )
    # oils
    engine_oil = models.PositiveBigIntegerField(null=True, verbose_name=_("Engine Oil"))
    gearbox_oil = models.PositiveBigIntegerField(
        null=True, verbose_name=_("Gearbox Oil")
    )
    hydraulic_fluid = models.PositiveBigIntegerField(
        null=True, verbose_name=_("Hydraulic Fluid")
    )
    hydraulic_fluid_updated_date = models.DateTimeField(null=True)
    # filters
    oil_filter = models.PositiveBigIntegerField(null=True, verbose_name=_("Oil Filter"))
    fuel_filter = models.PositiveBigIntegerField(
        null=True, verbose_name=_("Fuel Filter")
    )
    air_filter = models.PositiveBigIntegerField(null=True, verbose_name=_("Air Filter"))
    cabin_air_filter = models.PositiveBigIntegerField(
        null=True, verbose_name=_("Cabin Air Filter")
    )
    # belts
    timing_belt = models.PositiveBigIntegerField(
        null=True, verbose_name=_("Timing Belt")
    )
    timing_belt_last_updated_date = models.DateTimeField(null=True)
    alternator_belt = models.PositiveBigIntegerField(
        null=True, verbose_name=_("Alternator Belt")
    )
    #
    front_brake_pads = models.PositiveBigIntegerField(
        null=True, verbose_name=_("Front Brake Pads")
    )
    rear_brake_pads = models.PositiveBigIntegerField(
        null=True, verbose_name=_("Rear Brake Pads")
    )
    spark_plug = models.PositiveBigIntegerField(null=True, verbose_name=_("Spark Plug"))
    front_suspension = models.PositiveBigIntegerField(
        null=True, verbose_name=_("Front Suspension")
    )
    clutch_plate = models.PositiveBigIntegerField(
        null=True, verbose_name=_("Clutch Plate")
    )

    def __str__(self):
        return str(self.id) + "-" + self.car.name + " id:" + str(self.car.id)


# --------------------------------------


class CarCustomSetup(models.Model):
    car = models.OneToOneField("Car", on_delete=models.CASCADE, related_name="setup")
    # oils
    engine_oil = models.PositiveBigIntegerField(default=ENGINE_OIL)
    hydraulic_fluid = models.PositiveBigIntegerField(default=HYDRAULIC_FLUID)
    gearbox_oil = models.PositiveBigIntegerField(default=GEARBOX_OIL)
    # filters
    oil_filter = models.PositiveBigIntegerField(default=OIL_FILTER)
    fuel_filter = models.PositiveBigIntegerField(default=FUEL_FILTER)
    air_filter = models.PositiveBigIntegerField(default=AIR_FILTER)
    cabin_air_filter = models.PositiveBigIntegerField(default=CABIN_AIR_FILTER)
    # belts
    timing_belt = models.PositiveBigIntegerField(default=TIMING_BELT)
    timing_belt_max_year = models.PositiveBigIntegerField(default=TIMING_BELT_MAX_YEAR)
    alternator_belt = models.PositiveBigIntegerField(default=ALTERNATOR_BELT)
    #
    front_brake_pads = models.PositiveBigIntegerField(default=FRONT_BRAKE_PAD)
    rear_brake_pads = models.PositiveBigIntegerField(default=REAR_BRAKE_PAD)
    spark_plug = models.PositiveBigIntegerField(default=SPARK_PLUG)
    front_suspension = models.PositiveBigIntegerField(default=FRONT_SUSPENSION)
    clutch_plate = models.PositiveBigIntegerField(default=CLUTCH_PLATE)

    def __str__(self):
        return str(self.id) + "-" + self.car.name + " car-id:" + str(self.car.id)


# --------------------------------------


class CustomFiled(models.Model):

    car = models.ForeignKey(
        "Car", on_delete=models.CASCADE, related_name="car_custom_fileds"
    )
    name = models.CharField(max_length=256)
    mileage_per_change = models.PositiveBigIntegerField(null=True)
    month_per_changes = models.PositiveBigIntegerField(null=True)
    #
    last_mileage_changed = models.PositiveBigIntegerField(null=True)
    last_date_changed = models.DateField(null=True)

    def __str__(self):
        return str(self.id) + "-" + self.name


# --------------------------------------


class CarCompany(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


# --------------------------------------


class CarModel(models.Model):
    unique_key = models.CharField(
        unique=True,
        default=functools.partial(secrets.token_urlsafe, nbytes=32),
        max_length=70,
    )
    name = models.CharField(max_length=256)
    car_company = models.ForeignKey(CarCompany, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk) + "-" + str(self.car_company) + "-" + self.name
