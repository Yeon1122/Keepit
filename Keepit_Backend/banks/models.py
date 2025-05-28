from django.db import models
from regions.models import RegionCity, RegionDistrict

class Bank(models.Model):
    BANK_CHOICES = [
        ('KB', 'KB국민은행'),
        ('SH', '신한은행'),
        ('WR', '우리은행'),
        ('NH', '농협은행'),
        ('IBK', '기업은행'),
        ('KEB', '하나은행'),
        ('SC', 'SC제일은행'),
        ('CT', '씨티은행'),
    ]

    name = models.CharField(max_length=100)
    bank_type = models.CharField(max_length=10, choices=BANK_CHOICES)
    address = models.CharField(max_length=200)
    region_city = models.ForeignKey(RegionCity, on_delete=models.CASCADE, related_name='banks')
    region_district = models.ForeignKey(RegionDistrict, on_delete=models.CASCADE, related_name='banks')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    phone = models.CharField(max_length=20, blank=True, null=True)
    operating_hours = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.get_bank_type_display()} - {self.name}"

    class Meta:
        ordering = ['bank_type', 'name']
