from django.contrib import admin
from .models import Bank

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['name', 'bank_type', 'region_city', 'region_district', 'address', 'phone']
    list_filter = ['bank_type', 'region_city', 'region_district']
    search_fields = ['name', 'address']
