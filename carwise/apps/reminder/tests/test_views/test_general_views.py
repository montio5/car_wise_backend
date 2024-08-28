# Standard Library
from datetime import timedelta
import json
from django.utils import timezone

# Django
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Third Party Packages
from rest_framework import status
from rest_framework.test import APIClient

# First Party Imports
from apps.reminder.models import CarCustomSetup
from apps.reminder.tests.factories import (
    CarFactory,
    CustomFiledFactory,
    MileageFactory,
)

CONTENT_TYPE = "application/json"
USERNAME = "john.smith"
TEST_POK = "1234@test"

# ____________________ Car Checker API Test _____________________ #


class CustomCheckAPITestCases(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = "check_data"
        cls.user = User.objects.create_superuser(username=USERNAME, password=TEST_POK)
        cls.car = CarFactory(user=cls.user)
        ten_years_ago = timezone.now() - timedelta(days=365 * 10)

        cls.mileage = MileageFactory(
            car=cls.car,
            mileage=100000,
            engine_oil=1,
            gearbox_oil=1,
            hydraulic_fluid=1,
            oil_filter=1,
            fuel_filter=1,
            air_filter=1,
            cabin_air_filter=1,
            timing_belt=1,
            alternator_belt=1,
            front_brake_pads=1,
            rear_brake_pads=1,
            spark_plug=1,
            front_suspension=1,
            clutch_plate=1,
            hydraulic_fluid_updated_date=ten_years_ago,
            timing_belt_last_updated_date=ten_years_ago,
        )
        cls.custom_fields_passed_mileage = CustomFiledFactory(
            car=cls.car, mileage_per_change=10, last_mileage_changed=1
        )
        cls.custom_fields_passed_date = CustomFiledFactory(
            car=cls.car, month_per_changes=10, last_date_changed=ten_years_ago
        )

        cls.setup = CarCustomSetup.objects.create(car=cls.car)

    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_tree_species_add_api(self):
        """Test car add api for unauthorized user"""
        self.client.force_authenticate(user=None)
        response = self.client.get(
            reverse(self.url),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorize_car_checker_api(self):
        """Test cars checker api for authorized user"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse(self.url),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(
        #     set(response.data.keys()),
        #     {
        #         "unique_key",
        #         "car_model",
        #         "car_model_display",
        #         "name",
        #         "custom_fields",
        #         "mileage_info",
        #     },
        # )
        # self.assertEqual(response.data["car_model"], self.data["car_model"])

    #     self.assertEqual(response.data["name"], self.data["name"])
    #     self.assertEqual(
    #         response.data["mileage_info"]["mileage"],
    #         self.data["mileage_info"]["mileage"],
    #     )
    #     self.assertEqual(
    #         response.data["mileage_info"]["engine_oil"],
    #         self.data["mileage_info"]["engine_oil"],
    #     )
    #     self.assertEqual(
    #         response.data["mileage_info"]["gearbox_oil"],
    #         self.data["mileage_info"]["gearbox_oil"],
    #     )
    #     self.assertEqual(
    #         response.data["mileage_info"]["hydraulic_fluid"],
    #         self.data["mileage_info"]["hydraulic_fluid"],
    #     )
    #     self.assertIn(
    #         self.data["mileage_info"]["hydraulic_fluid_updated_date"],
    #         response.data["mileage_info"]["hydraulic_fluid_updated_date"],
    #     )
    #     self.assertEqual(
    #         response.data["mileage_info"]["fuel_filter"],
    #         self.data["mileage_info"]["fuel_filter"],
    #     )
    #     self.assertEqual(
    #         response.data["mileage_info"]["air_filter"],
    #         self.data["mileage_info"]["air_filter"],
    #     )
    #     self.assertEqual(
    #         response.data["mileage_info"]["cabin_air_filter"],
    #         self.data["mileage_info"]["cabin_air_filter"],
    #     )
    #     self.assertEqual(
    #         response.data["mileage_info"]["timing_belt"],
    #         self.data["mileage_info"]["timing_belt"],
    #     )
    #     self.assertEqual(
    #         response.data["mileage_info"]["spark_plug"],
    #         self.data["mileage_info"]["spark_plug"],
    #     )
    #     self.assertEqual(
    #         response.data["mileage_info"]["front_suspension"],
    #         self.data["mileage_info"]["front_suspension"],
    #     )
    #     self.assertEqual(
    #         response.data["mileage_info"]["clutch_plate"],
    #         self.data["mileage_info"]["clutch_plate"],
    #     )

    # def test_authorizecar_add_api_with_element_more_than_mileage(self):
    #     """Test car add api for authorized user"""
    #     self.client.force_authenticate(user=self.user)
    #     self.data["mileage_info"]["air_filter"] = (
    #         self.data["mileage_info"]["mileage"] + 1
    #     )
    #     response = self.client.post(
    #         reverse(self.url),
    #         data=json.dumps(self.data),
    #         content_type=CONTENT_TYPE,
    #     )

    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_authorizecar_add_api_with_no_mileage(self):
    #     """Test car add api for authorized user"""
    #     self.client.force_authenticate(user=self.user)
    #     self.data.pop("mileage_info")
    #     response = self.client.post(
    #         reverse(self.url),
    #         data=json.dumps(self.data),
    #         content_type=CONTENT_TYPE,
    #     )

    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_authorizecar_add_api_with_no_mileage(self):
    #     """Test car add api for authorized user"""
    #     self.client.force_authenticate(user=self.user)
    #     self.data["mileage_info"]["air_filter"] = -1
    #     response = self.client.post(
    #         reverse(self.url),
    #         data=json.dumps(self.data),
    #         content_type=CONTENT_TYPE,
    #     )

    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
