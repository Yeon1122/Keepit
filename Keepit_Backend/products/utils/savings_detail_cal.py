# 정기 예금, 적금 찜한 상품 비교
def calc_deposit_final_amount(total_amount, months, interest_rate):
    """
    정기예금 만기 금액 계산
    total_amount: 예금 금액
    months: 예금 기간 (개월)
    interest_rate: 연 이자율 (%)
    """
    if not all(isinstance(x, (int, float)) for x in [total_amount, months, interest_rate]):
        return 0
    
    if total_amount <= 0 or months <= 0 or interest_rate < 0:
        return 0

    # 단리 계산: 원금 + 이자
    rate = interest_rate / 100
    interest = total_amount * rate * (months / 12)
    return round(total_amount + interest)

    # 적금
def calc_saving_final_amount(monthly_amount, months, interest_rate):
    """
    적금 만기 금액 계산
    monthly_amount: 월 적금액
    months: 적금 기간 (개월)
    interest_rate: 연 이자율 (%)
    """
    if not all(isinstance(x, (int, float)) for x in [monthly_amount, months, interest_rate]):
        return 0
    
    if monthly_amount <= 0 or months <= 0 or interest_rate < 0:
        return 0

    rate = interest_rate / 100
    total = 0
    for i in range(months):
        # 매월 납입금에 대한 이자 계산 (단리)
        # i개월째 납입금은 (months-i)개월 동안 이자가 붙음
        interest_period = (months - i) / 12  # 이자계산기간(연)
        this_month_amount = monthly_amount * (1 + rate * interest_period)
        total += this_month_amount
    
    return round(total)

# products/utils/savings_detail_cal.py

def filter_one_option_per_product(matched_products, preferred_months):
    """
    각 상품별로 가장 적합한 옵션 하나를 선택
    1. 각 상품의 실제 가능한 기간 중에서 선택
    2. 선호하는 기간과 정확히 일치하는 옵션 우선
    3. 일치하는 옵션이 없으면 가장 가까운 기간의 옵션 선택
    4. 같은 기간이면 금리가 높은 옵션 선택
    """
    if not matched_products:
        return []

    # 선호 기간이 유효하지 않으면 기본값 12개월 사용
    if preferred_months <= 0:
        preferred_months = 12

    # 상품별로 그룹화
    products_by_name = {}
    for p in matched_products:
        name = p["name"]
        if name not in products_by_name:
            products_by_name[name] = []
        products_by_name[name].append(p)

    result = {}
    # 각 상품별로 처리
    for name, options in products_by_name.items():
        # 해당 상품의 가능한 기간들
        available_terms = sorted([opt["term"] for opt in options])
        if not available_terms:
            continue

        # 1. 정확히 일치하는 기간 찾기
        matching_options = [opt for opt in options if opt["term"] == preferred_months]
        if matching_options:
            # 같은 기간이면 금리가 높은 것 선택
            result[name] = max(matching_options, key=lambda x: x["interest_rate"])
            continue

        # 2. 가장 가까운 기간 찾기
        closest_term = min(available_terms, key=lambda x: abs(x - preferred_months))
        closest_options = [opt for opt in options if opt["term"] == closest_term]
        # 같은 기간이면 금리가 높은 것 선택
        result[name] = max(closest_options, key=lambda x: x["interest_rate"])

    # 결과가 없으면 각 상품의 첫 번째 옵션 선택
    if not result:
        for name, options in products_by_name.items():
            if options:
                result[name] = max(options, key=lambda x: x["interest_rate"])

    return list(result.values())
