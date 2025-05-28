import pandas as pd
import random
import os

# 절대 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')
os.makedirs(DATA_DIR, exist_ok=True)

def generate_user_data(n=100):
    # 범주형 변수 후보
    genders = ['M', 'F']
    risks = ['low', 'medium', 'high']
    goals = ['단기 여행', '결혼 준비', '내 집 마련', '은퇴 준비', '목돈 마련']
    financial_knowledge_levels = ['낮음', '보통', '높음']
    investment_experiences = ['없음', '1~3년', '3년 이상']
    user_types = ['사회초년생', '직장인', '주부', '은퇴자']
    preferred_terms = ['단기', '중기', '장기']

    users = []
    labels = []

    for uid in range(1, n + 1):
        # 유저 정보 랜덤 생성
        age = random.randint(20, 60)
        gender = random.choice(genders)
        income = random.randint(2000, 10000)
        assets = random.randint(1000, 50000)
        risk = random.choice(risks)
        goal = random.choice(goals)
        fin_know = random.choice(financial_knowledge_levels)
        invest_exp = random.choice(investment_experiences)
        user_type = random.choice(user_types)
        term = random.choice(preferred_terms)

        users.append({
            "user_id": uid,
            "age": age,
            "gender": gender,
            "income": income,
            "assets": assets,
            "risk_tolerance": risk,
            "saving_goal": goal,
            "financial_knowledge": fin_know,
            "investment_experience": invest_exp,
            "user_type": user_type,
            "preferred_term": term,
        })

        # 추천 카테고리 라벨 생성 (rule-based)
        deposit = 1 if risk == 'low' or goal in ['내 집 마련', '은퇴 준비'] else 0
        saving = 1 if income < 6000 and risk != 'high' else 0
        stock = 1 if risk == 'high' or invest_exp == '3년 이상' else 0
        etf = 1 if risk in ['medium', 'high'] and fin_know == '높음' else 0
        goods = 1 if assets >= 10000 and fin_know != '낮음' else 0

        labels.append({
            "user_id": uid,
            "deposit": deposit,
            "saving": saving,
            "stock": stock,
            "etf": etf,
            "goods": goods
        })

    return pd.DataFrame(users), pd.DataFrame(labels)

if __name__ == '__main__':
    users_df, labels_df = generate_user_data(100)
    full_df = pd.merge(users_df, labels_df, on='user_id')
    
    # 데이터 저장
    output_path = os.path.join(DATA_DIR, 'user_category_training_data.csv')
    full_df.to_csv(output_path, index=False)
    print(f"데이터가 저장되었습니다: {output_path}")