from rest_framework import serializers
from .models import TestResult

class TestResultSerializer(serializers.ModelSerializer):
    result_description = serializers.SerializerMethodField()
    risk_type_display = serializers.CharField(source='get_risk_type_display', read_only=True)
    user_id = serializers.CharField(source='user.userid', read_only=True)

    class Meta:
        model = TestResult
        fields = [
            'id', 'user_id', 'risk_type', 'risk_type_display', 
            'total_score', 'result_description',
            'q1_age', 'q2_experience', 'q3_loss_response',
            'q4_income', 'q5_expected_return', 'q6_emergency',
            'created_at'
        ]
        read_only_fields = ['user_id', 'risk_type', 'risk_type_display', 'total_score']

    def get_result_description(self, obj):
        return obj.result_description 