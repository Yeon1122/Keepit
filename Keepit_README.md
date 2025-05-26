# 내 손 안의 금융 비서 - Keepit (킵잇)

> **SSAFY 13기 대전 2반 10팀 송영지, 이하연**  
> 본 프로젝트는 SSAFY 과정 중 개발된 팀 프로젝트입니다.

---

## 📖 프로젝트 개요

**Keepit**은 예·적금, 주식, ETF, 현물(금·은) 상품 정보를 한눈에 비교·분석할 수 있는 **올인원** 금융 플랫폼입니다.  

사용자 투자 성향에 따라 **맞춤형 상품을 추천**하고, 주변 은행 위치 검색, 금융 커뮤니티, AI 챗봇 상담 등 폭넓은 기능을 제공합니다.  
금융 초보자부터 투자 고수까지 모두 사용할 수 있도록 직관적 UI와 신뢰도 높은 데이터를 목표로 개발되었습니다.

---

## 주요 기능

### 1. 투자 성향 테스트 (ML 기반)
- ML 기반 모델을 활용한 투자 성향 테스트 및 맞춤 추천

### 2. 금융 상품 탐색
- 예·적금 금리 비교 및 상세 정보 조회
- 금·은 등 현물 정보 제공
- 주식/ETF 실시간 정보 제공
- 관심 상품 찜하기

### 3. 찜한 상품 비교하기
- 예·적금, 주식, ETF 등 사용자가 찜한 상품을 최대 2개까지 비교 기능 제공
- 금융 커뮤니티
- 자유게시판·질문게시판 운영
- 게시글/댓글 CRUD, 좋아요, 실시간 반영

### 4. 사용자 커스터마이징
- 프로필, 회원 정보 수정
- 팔로우/팔로워 기능

### 5. 은행 찾기
- 위치 기반 주변 은행 검색 및 정보 제공

### 6. 챗봇 상담
- 홈페이지·금융상품 문의
- AI 기반 실시간 답변 및 정보 제공
- 대화 세션 관리

---

## 기술 스택

| 구분       | 기술                                    |
|------------|-----------------------------------------|
| 프론트엔드 | Vue 3, Pinia, Vue Router, Axios         |
| 백엔드     | Django, Django REST Framework                   |
| DB         | SQLite (개발용)                         |
| 기타 도구  | GitHub, Figma, Notion                   |

---

## 폴더 구조
```
Keepit/
├── Keepit_Backend/
│   ├── banks/                  # 은행 정보 및 위치 데이터
│   ├── chatbot/                # AI 챗봇 기능
│   ├── community/              # 커뮤니티(게시판) 기능
│   ├── keepit/                 # Django 설정
│   │   └── settings.py
│   ├── news/                   # 금융 뉴스 기능
│   ├── products/               # 금융 상품(예적금, 주식 등)
│   ├── regions/                # 지역/은행 위치 검색
│   ├── scripts/                # 데이터 로딩, 크롤링 등 스크립트
│   ├── tests/                  # 투자 성향 테스트, 추천 기능
│   └── users/                  # 회원 관리
│
├── Keepit_Frontend/
│   ├── public/
│   │   └── images/
│   │         ├── images_bank/  # 은행 로고 등
│   │         ├── images_momo/  # 캐릭터/마스코트
│   │         └── images_logo/  # 서비스 로고
│   ├── src/
│   │   ├── assets/
│   │   │     ├── data/
│   │   │     │     ├── bankLinks.json
│   │   │     │     ├── birthDropdown.json
│   │   │     │     └── mapInfo.json
│   │   │     └── images/
│   │   ├── components/         # 재사용 Vue 컴포넌트
│   │   ├── stores/             # Pinia 상태관리
│   │   ├── router/             # Vue Router 설정
│   │   └── views/              # 라우팅 페이지 컴포넌트
│
├── docs/
│   ├── Keepit_요구사항 명세서/
│   ├── Keepit_사용자 플로우 다이어그램/
│   ├── Keepit_ERD 다이어그램/
│   ├── Keepit_와이어 프레임/
│   └── Keepit_API 명세서/
│
└── README.md
```
---

## 설치 및 실행 방법

### 프론트엔드
```bash
cd Keepit_Frontend
npm install
npm run dev
```
- `.env.example` 파일 참고해 `.env` 파일 생성 (API Key 관리)

### 백엔드
```bash
cd Keepit_Backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py shell
exec(open('scripts/load_regions.py', encoding='utf-8').read()) # 지역 데이터 등록
exit()
python manage.py runserver
```
- `.env.example` 파일 참고해 `.env` 파일 생성 (API Key 관리)

---

## 주요 페이지 안내

| URL                              | 설명                                   |
|----------------------------------|----------------------------------------|
| `/home`                          | 메인 홈                                |
| `/products/deposits`             | 정기 예금 상품 정보                    |
| `/products/savings`              | 적금 상품 정보                         |
| `/products/goods`                | 현물(금·은) 정보                       |
| `/products/stocks`               | 주식 정보                              |
| `/products/etfs`                 | ETF 정보                               |
| `/products/compare/deposits`     | 정기 예금 상품 비교                    |
| `/products/compare/savings`      | 적금 상품 비교                         |
| `/banks/nearby`                  | 내 위치 기반 은행 검색                 |
| `/community`                     | 자유게시판/질문게시판                  |
| `/profile`                       | 사용자 프로필 및 성향 설정             |
| `/users`                         | 로그인, 회원가입, 마이페이지 등        |
| `/chatbot`                       | 챗봇 상담                              |
| `/test`                          | 투자 성향 테스트                       |

---

## 외부 API 연동

| 기능             | API 출처                     |
|------------------|------------------------------|
| 정기 예금/적금   | 금융감독원 오픈 API          |
| 현물             | Goid API.io                  |
| 주식/ETF         | 한국투자증권 Open API        |
| 주식 관련 뉴스   | NAVER Developers             |
| 은행 위치        | Kakao Map API                |
| AI 챗봇          | OpenAI API                   |

---

## 협업 및 Git 전략

- **Git flow** 기반 브랜치 전략
  - `main`: 배포 브랜치
  - `dev`: 개발 통합 브랜치
  - `기능명`: 기능별 개발 브랜치
- **협업 툴**: Notion으로 업무 분배 및 이력 관리
- **디자인**: Figma 와이어프레임 기반 구현

---

## 향후 개선 사항

- 소셜 로그인(OAuth) 연동
- 금융 상품 추천 알고리즘 고도화
- 실시간 채팅 챗봇 기능 강화
- 관리자 대시보드 구축
- 투자 리포트/포트폴리오 기능 추가

---

## 기여자

| 이름   | 역할                                               |
|--------|----------------------------------------------------|
| **송영지** | 백엔드, 기획, API 연동, 상품 추천 알고리즘         |
| **이하연** | 프론트엔드, 기획, API 연동, UI/UX 설계             |

---

## 소감

### 송영지
소감

### 이하연
소감

---
