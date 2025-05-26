# news/models.py
from django.db import models

class StockNews(models.Model):
    stock_code = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    link = models.URLField()
    published_at = models.DateTimeField()

    def __str__(self):
        return f"[{self.stock_code}] {self.title}"
