## 초기 설정 방법

1. 가상환경 설치 및 활성화
    ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```

2. `pip install -r requirements.txt`

3. 마이그레이션
    ```bash
    python manage.py migrate
    ```

4. 지역 데이터 등록
    ```
    python manage.py shell
    exec(open('scripts/load_regions.py', encoding='utf-8').read())
    ```