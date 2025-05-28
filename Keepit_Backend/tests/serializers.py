from rest_framework import serializers
from .models import TestResult

class TestResultSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.userid', read_only=True)

    class Meta:
        model = TestResult
        fields = [
            'id', 'user_id', 'risk_type', 'test_data', 'created_at'
        ]
        read_only_fields = ['user_id', 'risk_type'] 