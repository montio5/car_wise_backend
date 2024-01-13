from django.db import models
import uuid
from django.contrib.auth.models import User

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
    unique_key = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # oils
    engine_oil = models.IntegerField(null=True)
    gearbox_oil = models.IntegerField(null=True)
    brake_fluid = models.IntegerField(null=True)
    hydraulic_fluid = models.IntegerField(null=True)
    hydraulic_fluid_updated_date = models.DateTimeField(null=True)
    # filters
    oil_filter = models.IntegerField(null=True)
    fuel_filter = models.IntegerField(null=True)
    air_filter = models.IntegerField(null=True)
    cabin_air_filter = models.IntegerField(null=True)
    cabin_air_filter_updated_date = models.DateTimeField(null=True)
    # belts
    timing_belt = models.IntegerField()
    alternator_belt = models.IntegerField()
    #
    front_brake_pads = models.IntegerField(null=True)
    rear_brake_pads = models.IntegerField(null=True)
    spark_plug = models.IntegerField(null=True)
    front_suspension = models.IntegerField(null=True)
    cooler_gas = models.IntegerField(null=True)
    clutch_plate = models.IntegerField(null=True)


# --------------------------------------


class CarCustomizeSetup(models.Model):
    car = models.OneToOneField("Car", on_delete=models.CASCADE)
    # oils
    engine_oil = models.IntegerField(default=ENGINE_OIL)
    brake_fluid = models.IntegerField(default=BRAKE_FLUID)
    hydraulic_fluid = models.IntegerField(default=HYDRAULIC_FLUID)
    # filters
    oil_filter = models.IntegerField(default=OIL_FILTER)
    fuel_filter = models.IntegerField(default=FUEL_FILTER)
    air_filter = models.IntegerField(default=AIR_FILTER)
    cabin_air_filter = models.IntegerField(default=CABIN_AIR_FILTER)
    # belts
    timing_belt = models.IntegerField(default=TIMING_BELT)
    alternator_belt = models.IntegerField(default=ALTERNATOR_BELT)
    #
    front_brake_pads = models.IntegerField(default=FRONT_BRAKE_PAD)
    rear_brake_pads = models.IntegerField(default=REAR_BRAKE_PAD)
    spark_plug = models.IntegerField(default=SPARK_PLUG)
    front_suspension = models.IntegerField(default=FRONT_SUSPENSION)
    cooler_gas_change_years = models.IntegerField(default=COOLER_GAS_CHANGE_YEARS)
    clutch_plate = models.IntegerField(default=CLUTCH_PLATE)


# --------------------------------------


class CarCompany(models.Model):
    car_company = models.CharField(max_length=256)


# --------------------------------------


class CarModel(models.Model):
    unique_key = models.UUIDField(primary_key=True, default=uuid.uuid4)
    car_model = models.CharField(max_length=256)
    car_company = models.ForeignKey(CarCompany, on_delete=models.CASCADE)
