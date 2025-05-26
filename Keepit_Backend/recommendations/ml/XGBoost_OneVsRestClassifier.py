import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
import joblib
import os

# 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw', 'user_category_training_data.csv')
MODEL_PATH = os.path.join(DATA_DIR, 'models', 'recommendation_model.pkl')

# 디렉토리 생성
os.makedirs(os.path.join(DATA_DIR, 'models'), exist_ok=True)

# 1. 데이터 불러오기
df = pd.read_csv(RAW_DATA_PATH)

# 2. 라벨 분리
y = df[['deposit', 'saving', 'stock', 'etf', 'goods']]
X = df.drop(columns=['user_id', 'deposit', 'saving', 'stock', 'etf', 'goods'])

# 3. 전처리: 범주형만 인코딩
categorical_cols = X.select_dtypes(include='object').columns.tolist()
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ],
    remainder='passthrough'  # 수치형은 그대로 사용
)

# 4. 모델 파이프라인 구성
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', OneVsRestClassifier(XGBClassifier(use_label_encoder=False, eval_metric='logloss')))
])

# 5. 학습/검증 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. 학습
model.fit(X_train, y_train)

# 7. 평가
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=y.columns))

# 8. 모델 저장
joblib.dump(model, MODEL_PATH)
print(f"모델이 저장되었습니다: {MODEL_PATH}")
