<template>
  <div class="result-container">
    <div v-if="loading" class="loading">
      결과를 불러오는 중입니다...
    </div>

    <div v-else-if="result" class="result-content">
      <h1 class="result-title">투자 성향 테스트 결과</h1>
      
      <div class="result-box">
        <div class="result-type">
          <h2>{{ result.type }}</h2>
          <div class="score">총점: {{ result.total_score }}점</div>
        </div>

        <div class="result-details">
          <div class="detail-item">
            <span class="label">나이대:</span>
            <span>{{ getAgeText(result.q1_age) }}</span>
          </div>
          <div class="detail-item">
            <span class="label">투자 경험:</span>
            <span>{{ getExperienceText(result.q2_experience) }}</span>
          </div>
          <div class="detail-item">
            <span class="label">손실 대응:</span>
            <span>{{ getLossResponseText(result.q3_loss_response) }}</span>
          </div>
          <div class="detail-item">
            <span class="label">수입원:</span>
            <span>{{ getIncomeText(result.q4_income) }}</span>
          </div>
          <div class="detail-item">
            <span class="label">기대 수익률:</span>
            <span>{{ getReturnText(result.q5_expected_return) }}</span>
          </div>
          <div class="detail-item">
            <span class="label">비상 자금:</span>
            <span>{{ getEmergencyText(result.q6_emergency) }}</span>
          </div>
        </div>

        <div class="result-description">
          <h3>성향 설명</h3>
          <ul>
            <li>{{ result.description.description }}</li>
            <li>{{ result.description.recommendation }}</li>
          </ul>
        </div>

        <div class="recommendation">
          <h3>추천 투자 방식</h3>
          <ul>
            <li v-for="(item, index) in result.recommendations" :key="index">
              {{ item }}
            </li>
          </ul>
        </div>

        <div class="product-navigator">
          <h3>추천 상품 바로가기</h3>
          <div class="nav-buttons">
            <router-link 
              :to="{ name: 'savings' }" 
              class="nav-btn"
              :class="{ 'highlight': result.type === '안정형 투자자' }"
              @click="scrollToTop"
            >
              정기예금/적금
            </router-link>
            <router-link 
              :to="{ name: 'goods' }" 
              class="nav-btn"
              :class="{ 'highlight': result.type === '중립형 투자자' }"
              @click="scrollToTop"
            >
              현물
            </router-link>
            <router-link 
              :to="{ name: 'stocks' }" 
              class="nav-btn"
              :class="{ 'highlight': result.type === '공격형 투자자' }"
              @click="scrollToTop"
            >
              주식
            </router-link>
          </div>
        </div>
      </div>

      <div class="action-buttons">
        <button @click="retakeTest" class="retake-btn">테스트 다시하기</button>
        <button @click="goToMyPage" class="mypage-btn">마이페이지로 이동</button>
      </div>
    </div>

    <div v-else class="error">
      결과를 불러오는데 실패했습니다.
      <button @click="retakeTest" class="retake-btn">테스트 다시하기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAccountStore } from '@/stores/users.js'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const accountStore = useAccountStore()
const loading = ref(true)
const result = ref(null)

const getAgeText = (value) => {
  const ages = ['20대 이하', '30~40대', '50대 이상']
  return ages[value - 1]
}

const getExperienceText = (value) => {
  const experiences = ['없음', '약간 있음', '매우 많음']
  return experiences[value - 1]
}

const getLossResponseText = (value) => {
  const responses = ['전부 인출', '일부 유지', '추가 매수']
  return responses[value - 1]
}

const getIncomeText = (value) => {
  const incomes = ['불안정 (자영업, 아르바이트 등)', '보통 (정규직 등)', '매우 안정 (공무원, 연금 등)']
  return incomes[value - 1]
}

const getReturnText = (value) => {
  const returns = ['3% 이하', '5~8%', '10% 이상']
  return returns[value - 1]
}

const getEmergencyText = (value) => {
  const emergencies = ['전혀 대비 안 됨', '일부 대비됨', '충분히 대비됨']
  return emergencies[value - 1]
}

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

onMounted(async () => {
  const token = accountStore.token
  if (!token) {
    alert('⚠️ 로그인이 필요한 서비스입니다.')
    router.push({ name: 'login' })
    return
  }

  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/test/result/', {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    result.value = res.data
  } catch (err) {
    if (err.response?.status === 404) {
      alert('테스트 결과가 없습니다. 테스트를 먼저 진행해주세요.')
      router.push({ name: 'investmenttest' })
      return
    }
    console.error('테스트 결과 로딩 실패:', err)
  } finally {
    loading.value = false
  }
})

const getRecommendations = (type) => {
  switch (type) {
    case '안정형':
      return [
        '원금 보장형 상품 위주로 투자',
        '정기예금, 적금 추천',
        '안정적인 채권형 펀드 고려'
      ]
    case '중립형':
      return [
        '적절한 위험-수익 균형 추구',
        '채권형과 주식형 펀드 혼합',
        '안정적인 배당주 투자 고려'
      ]
    case '공격형':
      return [
        '높은 수익을 위한 적극적 투자',
        '주식형 펀드, 해외 투자',
        '신흥 시장 및 섹터 투자 고려'
      ]
    default:
      return []
  }
}

const retakeTest = async () => {
  console.log('🎯 테스트 결과 페이지 - 테스트 다시하기 버튼 클릭됨')
  
  // 이미 결과가 있다는 것을 알고 있으므로 바로 확인창 표시
  const userChoice = confirm('이미 투자 성향 검사를 받으셨습니다.\n\n다시 검사를 받으시겠습니까?\n\n확인: 새로 검사받기\n취소: 현재 결과 유지')
  console.log('👤 사용자 선택:', userChoice ? '새로 검사받기' : '현재 결과 유지')
  
  if (userChoice) {
    // 새로 검사받기
    router.push({ name: 'investmenttest' })
    scrollToTop()
  }
  // 취소하면 현재 페이지에 그대로 유지
}

const goToMyPage = () => {
  router.push({ name: 'mypage' })
  scrollToTop()
}
</script>

<style scoped>
.result-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.result-title {
  text-align: center;
  color: #145c2b;
  margin-bottom: 2rem;
}

.result-box {
  background: white;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.result-type {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #145c2b;
}

.result-type h2 {
  color: #145c2b;
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.score {
  color: #666;
  font-size: 1.1rem;
}

.result-details {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.8rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid #e9ecef;
}

.detail-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.detail-item .label {
  font-weight: bold;
  color: #495057;
}

.result-description, .recommendation {
  margin-bottom: 1.5rem;
}

.result-description h3, .recommendation h3 {
  color: #333;
  margin-bottom: 1rem;
}

.result-description ul {
  list-style: none;
  padding: 0;
}

.result-description li {
  padding: 0.5rem 0;
  padding-left: 1.5rem;
  position: relative;
}

.recommendation ul {
  list-style: none;
  padding: 0;
}

.recommendation li {
  padding: 0.5rem 0;
  padding-left: 1.5rem;
  position: relative;
}

.recommendation li::before {
  content: "•";
  color: #145c2b;
  position: absolute;
  left: 0;
}

.product-navigator {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid #e9ecef;
}

.product-navigator h3 {
  text-align: center;
  margin-bottom: 1.5rem;
}

.nav-buttons {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.nav-btn {
  flex: 1;
  padding: 1rem;
  text-align: center;
  text-decoration: none;
  color: #495057;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  background: #e9ecef;
  transform: translateY(-2px);
}

.nav-btn.highlight {
  background: #145c2b;
  color: white;
  border-color: #145c2b;
}

.nav-btn.highlight:hover {
  background: #0d4420;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.retake-btn, .mypage-btn {
  padding: 0.8rem 1.5rem;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.retake-btn {
  background-color: white;
  color: #145c2b;
  border: 2px solid #145c2b;
}

.mypage-btn {
  background-color: #145c2b;
  color: white;
  border: none;
}

.retake-btn:hover {
  background-color: #145c2b;
  color: white;
}

.mypage-btn:hover {
  background-color: #0d4420;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}
</style> 