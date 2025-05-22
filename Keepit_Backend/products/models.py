from django.db import models

PRODUCT_TYPES = (
    ('deposit', '정기예금'),
    ('saving', '적금'),
    ('stock', '주식'),
    ('etf','ETF'),
    ('goods','현물')
)

class Product(models.Model):
    # 상품 유형: deposit(정기예금), saving(적금), stock(주식), etf(ETF), goods(현물)
    type = models.CharField(max_length=10, choices=PRODUCT_TYPES)

    # 공통 필드
    name = models.CharField(max_length=100) # 상품 이름 또는 종목명
    company = models.CharField(max_length=100, blank=True, null=True)  # 금융사 이름(예/적금) 또는 발행사(주식/ETF)
    link = models.URLField(blank=True)

    # 예금/적금용 필드
    interest_rate = models.FloatField(blank=True, null=True)
    special_rate = models.FloatField(blank=True, null=True)
    term = models.CharField(max_length=100, blank=True, null=True)
    target = models.CharField(max_length=100, blank=True, null=True)

    # 주식/ETF용 필드
    stock_code = models.CharField(max_length=20, blank=True, null=True)  # 종목코드
    market_type = models.CharField(max_length=50, blank=True, null=True)  # 코스피, 코스닥 등
    
    # 주식만을 위한 필드
    current_price = models.FloatField(blank=True, null=True)
    price_change = models.FloatField(blank=True, null=True)
    sector = models.CharField(max_length=10)
    warning_info = models.TextField(max_length=300, blank=True, null=True)

    open_price = models.FloatField(blank=True, null=True)
    high_price = models.FloatField(blank=True, null=True)
    low_price = models.FloatField(blank=True, null=True)
    base_price = models.FloatField(blank=True, null=True)
    weighted_avg_price = models.FloatField(blank=True, null=True)

    high_52w = models.FloatField(blank=True, null=True)
    high_52w_date = models.DateField()
    low_52w = models.FloatField(blank=True, null=True)
    low_52w_date = models.DateField()


    # ETF만을 위한 필드
    index = models.CharField(max_length=100, blank=True, null=True)  # 추종지수
    nav = models.FloatField(blank=True, null=True)  # 순자산가치

    def __str__(self):
        return f"[{self.get_product_type_display()}] {self.name}"