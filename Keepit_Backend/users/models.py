from django.contrib.auth.models import AbstractUser
from django.db import models
from regions.models import RegionCity, RegionDistrict

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=10)
    nickname = models.CharField(max_length=32, unique=True)
    userid = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    region_city = models.ForeignKey(RegionCity, on_delete = models.SET_NULL, null=True)
    region_district = models.ForeignKey(RegionDistrict, on_delete=models.SET_NULL, null=True)