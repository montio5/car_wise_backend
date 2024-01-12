from django.db import models
import uuid
from django.contrib.auth.models import User


# --------------------------------------
class Car(models.Model):
    unique_key = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# --------------------------------------


class CarCompany(models.Model):
    car_company = models.CharField(max_length=256)


# --------------------------------------


class CarModel(models.Model):
    unique_key = models.UUIDField(primary_key=True, default=uuid.uuid4)
    car_model = models.CharField(max_length=256)
    car_company = models.ForeignKey(CarCompany, on_delete=models.CASCADE)
