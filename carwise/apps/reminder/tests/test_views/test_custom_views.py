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
USERNAME = "john.smith"
TEST_POK = "1234@test"


# ____________________ Custom Field Add API Test _____________________ #


class CustomFieldAddAPITestCases(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = "add_custom_field"
        cls.user = User.objects.create_superuser(username=USERNAME, password=TEST_POK)
        cls.car = CarFactory(user=cls.user)
        cls.mileage = MileageFactory(car=cls.car)
        cls.custom_field = CustomFiledFactory(car=cls.car)

        cls.data = {
            "name": "string",
            "mileage_per_change": 2123,
            "month_per_changes": 12,
            "last_mileage_changed": 1,
            "last_date_changed": "2024-02-26",
        }

    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_custom_field_add_api(self):
        """Test cusom field add api for unauthorized user"""
        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse(self.url, kwargs={"car_unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorize_custom_field_add_api(self):
        """Test cusom field add api for authorized user"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse(self.url, kwargs={"car_unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            set(response.data.keys()),
            {
                "id",
                "name",
                "mileage_per_change",
                "month_per_changes",
                "last_mileage_changed",
                "last_date_changed",
            },
        )
        # self.assertEqual(response.data["car_model"], self.data["car_model"])
        # self.assertEqual(response.data["name"], self.data["name"])
        # self.assertEqual(
        #     response.data["mileage_info"]["mileage"],
        #     self.data["mileage_info"]["mileage"],
        # )
        # self.assertEqual(
        #     response.data["mileage_info"]["engine_oil"],
        #     self.data["mileage_info"]["engine_oil"],
        # )
        # self.assertEqual(
        #     response.data["mileage_info"]["gearbox_oil"],
        #     self.data["mileage_info"]["gearbox_oil"],
        # )
        # self.assertEqual(
        #     response.data["mileage_info"]["brake_fluid"],
        #     self.data["mileage_info"]["brake_fluid"],
        # )
        # self.assertEqual(
        #     response.data["mileage_info"]["hydraulic_fluid"],
        #     self.data["mileage_info"]["hydraulic_fluid"],
        # )
        # self.assertIn(
        #     self.data["mileage_info"]["hydraulic_fluid_updated_date"],
        #     response.data["mileage_info"]["hydraulic_fluid_updated_date"],
        # )
        # self.assertEqual(
        #     response.data["mileage_info"]["fuel_filter"],
        #     self.data["mileage_info"]["fuel_filter"],
        # )
        # self.assertEqual(
        #     response.data["mileage_info"]["air_filter"],
        #     self.data["mileage_info"]["air_filter"],
        # )
        # self.assertEqual(
        #     response.data["mileage_info"]["cabin_air_filter"],
        #     self.data["mileage_info"]["cabin_air_filter"],
        # )
        # self.assertIn(
        #     self.data["mileage_info"]["cabin_air_filter_updated_date"],
        #     response.data["mileage_info"]["cabin_air_filter_updated_date"],
        # )
        # self.assertEqual(
        #     response.data["mileage_info"]["timing_belt"],
        #     self.data["mileage_info"]["timing_belt"],
        # )
        # self.assertEqual(
        #     response.data["mileage_info"]["spark_plug"],
        #     self.data["mileage_info"]["spark_plug"],
        # )
        # self.assertEqual(
        #     response.data["mileage_info"]["front_suspension"],
        #     self.data["mileage_info"]["front_suspension"],
        # )
        # self.assertEqual(
        #     response.data["mileage_info"]["cooler_gas"],
        #     self.data["mileage_info"]["cooler_gas"],
        # )
        # self.assertEqual(
        #     response.data["mileage_info"]["clutch_plate"],
        #     self.data["mileage_info"]["clutch_plate"],
        # )

    def test_authorizecar_add_api_with_element_more_than_mileage(self):
        """Test cusom field add api for authorized user"""
        self.client.force_authenticate(user=self.user)
        self.data["last_mileage_changed"] = self.mileage.mileage + 1
        response = self.client.post(
            reverse(self.url, kwargs={"car_unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorizecar_add_api_with_no_mileage(self):
        """Test cusom field add api for authorized user"""
        self.client.force_authenticate(user=self.user)
        self.data.pop("mileage_per_change")
        self.data.pop("month_per_changes")

        response = self.client.post(
            reverse(self.url, kwargs={"car_unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorizecar_add_api_with_no_mileage(self):
        """Test cusom field add api for authorized user"""
        self.client.force_authenticate(user=self.user)
        self.data["mileage_per_change"] = -1
        response = self.client.post(
            reverse(self.url, kwargs={"car_unique_key": self.car.unique_key}),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# _____________________ Custom Field Update Destroy API Test ______________________ #
class CustomFieldUpdateDeleteAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(username=USERNAME, password=TEST_POK)
        cls.car = CarFactory(user=cls.user)
        cls.custom_field = CustomFiledFactory(car=cls.car)
        cls.mileage = MileageFactory(car=cls.car)
        #
        cls.client = APIClient()
        cls.url = "custom_field_edit_delete"
        cls.data = {
            "name": "string",
            "mileage_per_change": 2123,
            "month_per_changes": 12,
            "last_mileage_changed": 1,
            "last_date_changed": "2024-02-26",
        }

    def test_unauthorized_get_custom_field_api(self):
        response = self.client.get(
            reverse(
                self.url,
                kwargs={
                    "car_unique_key": self.car.unique_key,
                    "id": self.custom_field.id,
                },
            ),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_get_custom_field_bad_request_api(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse(
                self.url, kwargs={"car_unique_key": self.car.unique_key, "id": 123456}
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authorized_get_custom_field_api(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse(
                self.url,
                kwargs={
                    "car_unique_key": self.car.unique_key,
                    "id": self.custom_field.id,
                },
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            set(response.data.keys()),
            {
                "id",
                "name",
                "mileage_per_change",
                "month_per_changes",
                "last_mileage_changed",
                "last_date_changed",
            },
        )

    def test_unauthorized_update_custom_field_api(self):
        response = self.client.put(
            reverse(
                self.url,
                kwargs={
                    "car_unique_key": self.car.unique_key,
                    "id": self.custom_field.id,
                },
            ),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_update_custom_field_bad_request_api(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            reverse(
                self.url, kwargs={"car_unique_key": self.car.unique_key, "id": 123456}
            ),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authorized_update_custom_field_api(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            reverse(
                self.url,
                kwargs={
                    "car_unique_key": self.car.unique_key,
                    "id": self.custom_field.id,
                },
            ),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authorize_custom_field_edit_api_with_element_more_than_mileage(self):
        """Test cusom field edit api for authorized user"""
        self.client.force_authenticate(user=self.user)
        self.data["last_mileage_changed"] = self.mileage.mileage + 1
        response = self.client.put(
            reverse(
                self.url,
                kwargs={
                    "car_unique_key": self.car.unique_key,
                    "id": self.custom_field.id,
                },
            ),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorize_custom_field_edit_api_with_no_mileage_or_change_month_amount(
        self,
    ):
        """Test cusom field edit api for authorized user"""
        self.client.force_authenticate(user=self.user)
        self.data.pop("mileage_per_change")
        self.data.pop("month_per_changes")

        response = self.client.put(
            reverse(
                self.url,
                kwargs={
                    "car_unique_key": self.car.unique_key,
                    "id": self.custom_field.id,
                },
            ),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorize_custom_field_edit_api_with_negative_int(self):
        """Test cusom field edit api for authorized user"""
        self.client.force_authenticate(user=self.user)
        self.data["mileage_per_change"] = -1
        response = self.client.put(
            reverse(
                self.url,
                kwargs={
                    "car_unique_key": self.car.unique_key,
                    "id": self.custom_field.id,
                },
            ),
            data=json.dumps(self.data),
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorized_custom_field_delete_api(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse(
                self.url,
                kwargs={
                    "car_unique_key": self.car.unique_key,
                    "id": self.custom_field.id,
                },
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(0, CustomFiled.objects.all().count())
