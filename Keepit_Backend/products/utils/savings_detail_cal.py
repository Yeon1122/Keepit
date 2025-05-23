# 정기 예금, 적금 찜한 상품 비교
def calc_deposit_final_amount(total_amount, months, interest_rate):
    # 단리 계산: 원금 + 이자
    rate = interest_rate / 100
    interest = total_amount * rate * (months / 12)
    return round(total_amount + interest, 2)

    # 적금
def calc_saving_final_amount(monthly_amount, months, interest_rate):
    rate = interest_rate / 100
    total = 0
    for i in range(months):
        # 첫 달에 넣은 돈은 12개월 동안 이자 받음 → 이자 기간 = months - i
        total += monthly_amount * (1 + rate * ((months - i) / 12))
    return round(total, 2)

# products/utils/savings_detail_cal.py

def filter_one_option_per_product(matched_products, preferred_months):
    result = {}
    for p in matched_products:
        name = p["name"]
        if name not in result:
            result[name] = p
        else:
            prev = result[name]
            if abs(p["term"] - preferred_months) < abs(prev["term"] - preferred_months):
                result[name] = p
    return list(result.values())
