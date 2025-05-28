from django.db import models
from django.conf import settings

# Create your models here.

class TestResult(models.Model):
    RISK_CHOICES = [
        ('conservative', '안정형'),
        ('moderate', '중립형'),
        ('aggressive', '공격형'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='test_results')
    risk_type = models.CharField(max_length=20, choices=RISK_CHOICES)
    test_data = models.JSONField(default=dict)  # 기본값을 빈 딕셔너리로 설정
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']  # 최신 결과가 먼저 오도록
        
    def __str__(self):
        return f"{self.user.userid}의 투자 성향: {self.get_risk_type_display()}"
    
    @property
    def result_description(self):
        if self.risk_type == 'conservative':
            return {
                'type': '안정형',
                'description': '원금 손실을 최소화하려는 성향으로, 예적금 중심의 투자를 선호합니다.',
                'recommendation': '예금, 적금, 국채 등 안전한 금융상품 위주로 투자하는 것이 좋습니다.'
            }
        elif self.risk_type == 'moderate':
            return {
                'type': '중립형',
                'description': '적당한 수준의 위험을 감수할 수 있는 성향으로, 안정성과 수익성의 균형을 추구합니다.',
                'recommendation': '펀드, 채권 등을 혼합한 포트폴리오 구성을 추천합니다.'
            }
        else:  # aggressive
            return {
                'type': '공격형',
                'description': '높은 수익을 추구하며 그에 따른 위험을 감수할 수 있는 성향입니다.',
                'recommendation': '주식, 해외자산, 암호화폐 등 고위험/고수익 자산에 투자할 수 있습니다.'
            }
