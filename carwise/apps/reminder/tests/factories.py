# Standard Library
import secrets
import datetime

# Django
from django.conf import settings
from django.utils import timezone
import random

# Third Party Packages
import factory
import factory.fuzzy

# First Party Imports

from apps.reminder.models import (
    Car,
    CarCompany,
    CarCustomSetup,
    CarModel,
    CustomFiled,
    Mileage,
)

PREFIX_SLUG_TEXT = "slug%d"


# --------------------------------------
class CarCompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarCompany

    name = factory.Faker("first_name")


# --------------------------------------
class CarModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarModel

    car_company = factory.SubFactory(CarCompanyFactory)
    name = factory.Faker("first_name")


# --------------------------------------
class CarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Car

    name = factory.Faker("name")
    car_model = factory.SubFactory(CarModelFactory)
    unique_key = factory.LazyAttribute(lambda _: secrets.token_urlsafe(32))
    created_date = factory.Faker('date_time_this_decade', tzinfo=None)


# --------------------------------------
class MileageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Mileage

    car = factory.SubFactory(CarFactory)
    mileage = factory.LazyAttribute(lambda x: random.randrange(1, 1000))
    #
    hydraulic_fluid_updated_date = factory.Faker("date_of_birth")
    #
    timing_belt_last_updated_date = factory.Faker("date_of_birth")
    created_date = factory.fuzzy.FuzzyDateTime(
        datetime.datetime(2023, 1, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime.now().replace(tzinfo=datetime.timezone.utc),
    )


# --------------------------------------
class CarCustomSetupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarCustomSetup

    car = factory.SubFactory(CarFactory)
    # Define default values for fields
    engine_oil = factory.Faker('random_number', digits=5)
    hydraulic_fluid = factory.Faker('random_number', digits=5)
    gearbox_oil = factory.Faker('random_number', digits=5)
    oil_filter = factory.Faker('random_number', digits=5)
    fuel_filter = factory.Faker('random_number', digits=5)
    air_filter = factory.Faker('random_number', digits=5)
    cabin_air_filter = factory.Faker('random_number', digits=5)
    timing_belt = factory.Faker('random_number', digits=5)
    timing_belt_max_year = factory.Faker('random_number', digits=5)
    alternator_belt = factory.Faker('random_number', digits=5)
    front_brake_pads = factory.Faker('random_number', digits=5)
    rear_brake_pads = factory.Faker('random_number', digits=5)
    spark_plug = factory.Faker('random_number', digits=5)
    front_suspension = factory.Faker('random_number', digits=5)
    clutch_plate = factory.Faker('random_number', digits=5)


# --------------------------------------
class CustomFiledFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomFiled

    car = factory.SubFactory(CarFactory)
    name = factory.Faker("first_name")
    mileage_per_change = factory.LazyAttribute(lambda x: random.randrange(100, 1000))
    month_per_changes = factory.LazyAttribute(lambda x: random.randrange(1, 12))
    #
    last_mileage_changed = factory.LazyAttribute(lambda x: random.randrange(100, 1000))
    last_date_changed = timezone.now().date() - timezone.timedelta(days=365)
