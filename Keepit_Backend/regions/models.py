from django.db import models

# Create your models here.
class RegionCity(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class RegionDistrict(models.Model):
    name = models.CharField(max_length=20)
    city = models.ForeignKey(RegionCity,on_delete=models.CASCADE, related_name='districts')

    class Meta:
        unique_together = ('name','city')

    def __str__(self):
        return f'{self.name} {self.city.name}'