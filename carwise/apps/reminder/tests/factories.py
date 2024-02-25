# Standard Library
import secrets

# Django
from django.conf import settings
from django.utils import timezone

# Third Party Packages
import factory

# First Party Imports

from carwise.apps.reminder.models import (
    Car,
    CarCompany,
    CarCustomSetup,
    CarModel,
    CustomFiled,
    Mileage,
)

PREFIX_SLUG_TEXT = "slug%d"


class CarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Car


class MileageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Mileage


class CarCustomSetupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarCustomSetup


class CustomFiledFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomFiled


class CarCompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarCompany


class CarModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarModel
