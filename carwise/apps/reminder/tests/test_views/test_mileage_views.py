# Standard Library
import json

# Django
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Third Party Packages
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

# First Party Imports
from apps.reminder.models import CustomFiled
from apps.reminder.tests.factories import (
    CarFactory,
    CustomFiledFactory,
    MileageFactory,
)

CONTENT_TYPE = "application/json"
USERNAME = "john.smit"
TEST_POK = "1234@test"
# ____________________ Mileage Add API Test _____________________ #


class MileageAddAPITestCases(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = "add_edit_get_mileage"
        cls.user = User.objects.create_superuser(username=USERNAME, password=TEST_POK)
        cls.car = CarFactory(user=cls.user)
        cls.mileage = MileageFactory(car=cls.car, air_filter=30, engine_oil=40)
        cls.data = {
            "mileage": 2147483647,
            "engine_oil": 2147483647,
            "gearbox_oil": 2147483647,
            "brake_fluid": 2147483647,
            "hydraulic_fluid": 2147483647,
            "hydraulic_fluid_updated_date": "2022-04-12",
            "oil_filter": 2147483647,
            "fuel_filter": 2147483647,
            "air_filter": 2147483647,
            "cabin_air_filter": 2147483647,
            "cabin_air_filter_updated_date": "2022-04-12",
            "timing_belt": 2147483647,
            "timing_belt_filter_updated_date": "2022-04-12",
            "alternator_belt": 2147483647,
            "front_brake_pads": 2147483647,
            "rear_brake_pads": 2147483647,
            "spark_plug": 2147483647,
            "front_suspension": 2147483647,
            "cooler_gas": 2147483647,
            "clutch_plate": 2147483647,
        }

    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_mileage_add_api(self):
        """Test mileage add api for unauthorized user"""
        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse(self.url, kwargs={"unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorize_mileage_add_api(self):
        """Test mileage add api for authorized user"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse(self.url, kwargs={"unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            set(response.data.keys()),
            {
                "id",
                "unique_key",
                "created_date",
                "mileage",
                "engine_oil",
                "gearbox_oil",
                "brake_fluid",
                "hydraulic_fluid",
                "hydraulic_fluid_updated_date",
                "oil_filter",
                "fuel_filter",
                "air_filter",
                "cabin_air_filter",
                "cabin_air_filter_updated_date",
                "timing_belt",
                "timing_belt_filter_updated_date",
                "alternator_belt",
                "front_brake_pads",
                "rear_brake_pads",
                "spark_plug",
                "front_suspension",
                "cooler_gas",
                "clutch_plate",
            },
        )

    def test_authorize_mileage_add_fail_api_less_mileage_than_before(self):
        """Test mileage add api for authorized user"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse(self.url, kwargs={"unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.data["mileage"] = self.mileage.mileage - 1
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorize_mileage_add_fail_api_less_mileage_than_before(self):
        """Test mileage add api for authorized user"""
        self.client.force_authenticate(user=self.user)
        self.data["mileage"] = self.mileage.mileage - 1
        response = self.client.post(
            reverse(self.url, kwargs={"unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorize_mileage_add_fail_api_less_field_amount_than_before(self):
        """Test mileage add api for authorized user"""
        self.client.force_authenticate(user=self.user)
        self.data["air_filter"] = self.mileage.air_filter - 1
        response = self.client.post(
            reverse(self.url, kwargs={"unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorize_mileage_add_use_previous_data_api(self):
        """Test mileage add api for authorized user"""
        self.client.force_authenticate(user=self.user)
        self.data.pop("engine_oil")
        response = self.client.post(
            reverse(self.url, kwargs={"unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["engine_oil"], self.mileage.engine_oil)

    def test_authorize_mileage_add_api_fail_field_grater_than_mileage(self):
        """Test mileage add api for authorized user"""
        """when the mileage is less than a int field"""
        self.client.force_authenticate(user=self.user)
        self.data["mileage"] = 2
        response = self.client.post(
            reverse(self.url, kwargs={"unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
