from django.contrib import admin
from .models import RegionCity, RegionDistrict

@admin.register(RegionCity)
class RegionCityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(RegionDistrict)
class RegionDistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'city']
    list_filter = ['city']
    search_fields = ['name', 'city__name']
