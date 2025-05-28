from django.contrib.auth.models import AbstractUser
from django.db import models
from regions.models import RegionCity, RegionDistrict
from django.conf import settings

class User(AbstractUser):
    username = None             #AbstractUser: uername, email, first_name, last_name 등 필요한데 안씀!
    name = models.CharField(max_length=10)
    nickname = models.CharField(max_length=32, unique=True)
    userid = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=254, unique=True)

    birth_year = models.PositiveIntegerField(null=True, blank=True)
    birth_month = models.PositiveIntegerField(null=True, blank=True)
    birth_day = models.PositiveIntegerField(null=True, blank=True)

    region_city = models.ForeignKey(RegionCity, on_delete=models.SET_NULL, null=True)
    region_district = models.ForeignKey(RegionDistrict, on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.userid

class Follow(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='following',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='followers',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.userid} → {self.to_user.userid}"