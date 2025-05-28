from django.contrib import admin
from .models import TestResult

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'risk_type', 'created_at']
    list_filter = ['risk_type', 'created_at']
    search_fields = ['user__userid', 'risk_type']
    readonly_fields = ['risk_type', 'test_data']
