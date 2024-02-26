# Standard Library
import json

# Django
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Third Party Packages
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

# First Party Imports
from apps.common.message import AppMessages
from apps.reminder.models import Car, CarCustomSetup, CustomFiled, Mileage
from apps.reminder.tests.factories import (
    CarCompanyFactory,
    CarFactory,
    CarModelFactory,
    CustomFiledFactory,
    MileageFactory,
)

CONTENT_TYPE = "application/json"
USERNAME = "john.smith"
TEST_POK = "1234@test"

# ____________________ Car Add API Test _____________________ #


class CarAddAPITestCases(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = "add_car"
        cls.user = User.objects.create_superuser(username=USERNAME, password=TEST_POK)
        cls.car_company = CarCompanyFactory()
        cls.car_model = CarModelFactory(car_company=cls.car_company)
        cls.data = {
            "car_model": cls.car_model.id,
            "name": "string",
            "mileage_info": {
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
            },
        }

    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_tree_species_add_api(self):
        """Test car add api for unauthorized user"""
        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse(self.url),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorize_tree_species_add_api(self):
        """Test car add api for authorized user"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse(self.url),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        # breakpoint()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            set(response.data.keys()),
            {
                "unique_key",
                "car_model",
                "car_model_display",
                "name",
                "custom_fields",
                "mileage_info",
            },
        )
        self.assertEqual(response.data["car_model"], self.data["car_model"])
        self.assertEqual(response.data["name"], self.data["name"])
        self.assertEqual(
            response.data["mileage_info"]["mileage"],
            self.data["mileage_info"]["mileage"],
        )
        self.assertEqual(
            response.data["mileage_info"]["engine_oil"],
            self.data["mileage_info"]["engine_oil"],
        )
        self.assertEqual(
            response.data["mileage_info"]["gearbox_oil"],
            self.data["mileage_info"]["gearbox_oil"],
        )
        self.assertEqual(
            response.data["mileage_info"]["brake_fluid"],
            self.data["mileage_info"]["brake_fluid"],
        )
        self.assertEqual(
            response.data["mileage_info"]["hydraulic_fluid"],
            self.data["mileage_info"]["hydraulic_fluid"],
        )
        self.assertIn(
            self.data["mileage_info"]["hydraulic_fluid_updated_date"],
            response.data["mileage_info"]["hydraulic_fluid_updated_date"],
        )
        self.assertEqual(
            response.data["mileage_info"]["fuel_filter"],
            self.data["mileage_info"]["fuel_filter"],
        )
        self.assertEqual(
            response.data["mileage_info"]["air_filter"],
            self.data["mileage_info"]["air_filter"],
        )
        self.assertEqual(
            response.data["mileage_info"]["cabin_air_filter"],
            self.data["mileage_info"]["cabin_air_filter"],
        )
        self.assertIn(
            self.data["mileage_info"]["cabin_air_filter_updated_date"],
            response.data["mileage_info"]["cabin_air_filter_updated_date"],
        )
        self.assertEqual(
            response.data["mileage_info"]["timing_belt"],
            self.data["mileage_info"]["timing_belt"],
        )
        self.assertEqual(
            response.data["mileage_info"]["spark_plug"],
            self.data["mileage_info"]["spark_plug"],
        )
        self.assertEqual(
            response.data["mileage_info"]["front_suspension"],
            self.data["mileage_info"]["front_suspension"],
        )
        self.assertEqual(
            response.data["mileage_info"]["cooler_gas"],
            self.data["mileage_info"]["cooler_gas"],
        )
        self.assertEqual(
            response.data["mileage_info"]["clutch_plate"],
            self.data["mileage_info"]["clutch_plate"],
        )

    def test_authorizecar_add_api_with_element_more_than_mileage(self):
        """Test car add api for authorized user"""
        self.client.force_authenticate(user=self.user)
        self.data["mileage_info"]["air_filter"] = (
            self.data["mileage_info"]["mileage"] + 1
        )
        response = self.client.post(
            reverse(self.url),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorizecar_add_api_with_no_mileage(self):
        """Test car add api for authorized user"""
        self.client.force_authenticate(user=self.user)
        self.data.pop("mileage_info")
        response = self.client.post(
            reverse(self.url),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorizecar_add_api_with_no_mileage(self):
        """Test car add api for authorized user"""
        self.client.force_authenticate(user=self.user)
        self.data["mileage_info"]["air_filter"] = -1
        response = self.client.post(
            reverse(self.url),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# _____________________ CarList API Test _____________________ #


class CarListAPITestCase(TestCase):
    """Test module for all cases of car list"""

    @classmethod
    def setUpTestData(cls):
        cls.url = "car_list"
        cls.user = User.objects.create_superuser(username=USERNAME, password=TEST_POK)
        cls.car_company = CarCompanyFactory()
        cls.car_model = CarModelFactory(car_company=cls.car_company)
        cls.cars = CarFactory.create_batch(10, car_model=cls.car_model, user=cls.user)

    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_tree_species_list(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(
            reverse(self.url),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_tree_species_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse(self.url),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)


# _____________________ Car Update Destroy API Test ______________________ #


class CarUpdateDeleteAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(username=USERNAME, password=TEST_POK)
        cls.car = CarFactory(user=cls.user)
        cls.mileage = MileageFactory(car=cls.car)
        cls.client = APIClient()
        cls.url = "car_edit_delete"
        cls.data = {
            "car_model": CarModelFactory().id,
            "name": "string",
            "mileage_info": {
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
            },
        }

    def test_unauthorized_get_car_api(self):
        response = self.client.get(
            reverse(self.url, kwargs={"unique_key": self.car.unique_key}),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_get_car_bad_request_api(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse(self.url, kwargs={"unique_key": "not-a-unique-key"}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authorized_get_car_api(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse(self.url, kwargs={"unique_key": self.car.unique_key}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            set(response.data.keys()),
            {
                "unique_key",
                "car_model",
                "car_model_display",
                "name",
                "custom_fields",
                "mileage_info",
            },
        )

    def test_unauthorized_update_car_api(self):
        response = self.client.put(
            reverse(self.url, kwargs={"unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_update_car_bad_request_api(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            reverse(self.url, kwargs={"unique_key": "not-a-unique-key"}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authorized_update_car_api(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            reverse(self.url, kwargs={"unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authorizecar_edit_api_with_element_more_than_mileage(self):
        """Test car edit api for authorized user"""
        self.client.force_authenticate(user=self.user)
        self.data["mileage_info"]["air_filter"] = (
            self.data["mileage_info"]["mileage"] + 1
        )
        response = self.client.put(
            reverse(self.url, kwargs={"unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorizecar_edit_api_with_no_mileage(self):
        """Test car edit api for authorized user"""
        self.client.force_authenticate(user=self.user)
        self.data.pop("mileage_info")
        response = self.client.put(
            reverse(self.url, kwargs={"unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorizecar_edit_api_with_negative_int(self):
        """Test car edit api for authorized user"""
        self.client.force_authenticate(user=self.user)
        self.data["mileage_info"]["air_filter"] = -1
        response = self.client.put(
            reverse(self.url, kwargs={"unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorized_car_delete_api(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse(self.url, kwargs={"unique_key": self.car.unique_key}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(0, Car.objects.all().count())
        self.assertEqual(0, Mileage.objects.all().count())
        self.assertEqual(0, CustomFiled.objects.all().count())
        self.assertEqual(0, CarCustomSetup.objects.all().count())


