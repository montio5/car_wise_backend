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

    name = factory.Faker("first_name")
    car_model = factory.SubFactory(CarModelFactory)


# --------------------------------------
class MileageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Mileage

    car = factory.SubFactory(CarFactory)
    mileage = factory.LazyAttribute(lambda x: random.randrange(1, 1000))
    #
    hydraulic_fluid_updated_date = factory.Faker("date_of_birth")
    #
    cabin_air_filter_updated_date = factory.Faker("date_of_birth")
    #
    timing_belt_filter_updated_date = factory.Faker("date_of_birth")
    created_date = factory.fuzzy.FuzzyDateTime(
        datetime.datetime(2023, 1, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime.now().replace(tzinfo=datetime.timezone.utc),
    )


# --------------------------------------
class CarCustomSetupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarCustomSetup

    car = factory.SubFactory(CarFactory)


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
