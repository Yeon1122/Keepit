from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
    PRODUCT_TYPES = (
        ('deposit', '정기예금'),
        ('saving', '적금'),
        ('stock', '주식'),
        ('etf', 'ETF'),
        ('goods', '현물'),
    )
    
    product_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    interest_rate = models.FloatField(null=True, blank=True)
    special_rate = models.FloatField(null=True, blank=True)
    term = models.IntegerField(null=True, blank=True)
    target = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('type', 'name', 'company')

    def __str__(self):
        return f"{self.name} ({self.company})"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    type = models.CharField(max_length=20)
    identifier = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'type', 'identifier')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s favorite {self.type}: {self.identifier}"