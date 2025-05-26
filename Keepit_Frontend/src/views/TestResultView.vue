<template>
  <div class="test-result">
    <div v-if="testResult" class="result-container">
      <h1 class="result-title">투자 성향 분석 결과</h1>

      <!-- 투자 성향 -->
      <section class="result-section risk-type">
        <h2>투자 성향</h2>
        <div class="risk-type-content">
          <div class="risk-type-badge" :class="testResult.risk_type">
            {{ getRiskTypeDisplay(testResult.risk_type) }}
          </div>
          <p class="risk-type-description">
            {{ getRiskTypeDescription(testResult.risk_type) }}
          </p>
        </div>
      </section>

      <!-- 테스트 응답 -->
      <section class="result-section test-answers">
        <h2>테스트 응답 내역</h2>
        <div class="answers-grid">
          <div v-for="(value, key) in testResult.test_data" :key="key" class="answer-item">
            <span class="answer-label">{{ getQuestionLabel(key) }}</span>
            <span class="answer-value">{{ value }}</span>
          </div>
        </div>
      </section>

      <!-- 추천 상품 -->
      <section class="result-section recommendations">
        <h2>맞춤 투자 상품 추천</h2>
        <div class="recommendation-items">
          <div 
            v-for="(isRecommended, type) in testResult.recommendations" 
            :key="type"
            class="recommendation-item"
            :class="{ 'recommended': isRecommended }"
            @click="goToProductPage(type)"
            :style="{ cursor: isRecommended ? 'pointer' : 'default' }"
          >
            <div class="product-info">
              <span class="product-type">{{ getProductTypeDisplay(type) }}</span>
              <span class="recommendation-status" :class="{ 'recommended': isRecommended }">
                {{ isRecommended ? '추천' : '비추천' }}
              </span>
            </div>
            <p class="product-description">
              {{ getProductDescription(type) }}
            </p>
          </div>
        </div>
      </section>

      <div class="action-buttons">
        <button @click="retakeTest" class="retake-button">
          테스트 다시하기
        </button>
      </div>
    </div>

    <div v-else class="no-result">
      <p>테스트 결과를 찾을 수 없습니다.</p>
      <button @click="goToTest" class="take-test-button">
        테스트 하러가기
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/users.js'
import axios from 'axios'

const router = useRouter()
const accountStore = useAccountStore()
const testResult = ref(null)

onMounted(async () => {
  // 1. 먼저 router state에서 결과 확인
  const state = router.currentRoute.value.state
  if (state && state.testResult) {
    testResult.value = state.testResult
    return
  }

  // 2. state에 없으면 API로 가져오기
  const token = accountStore.token
  if (!token) {
    alert('로그인이 필요한 서비스입니다.')
    router.push({ name: 'login' })
    return
  }

  try {
    const response = await axios.get('/api/v1/test/result/', {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    
    if (response.data) {
      testResult.value = response.data
    } else {
      alert('테스트 결과가 없습니다. 테스트를 먼저 진행해주세요.')
      router.push({ name: 'investmenttest' })
    }
  } catch (err) {
    console.error('테스트 결과 로딩 실패:', err)
    if (err.response?.status === 404) {
      alert('테스트 결과가 없습니다. 테스트를 먼저 진행해주세요.')
      router.push({ name: 'investmenttest' })
    } else {
      alert('테스트 결과를 불러오는데 실패했습니다.')
    }
  }
})

const getRiskTypeDisplay = (riskType) => {
  const types = {
    conservative: '안정형',
    moderate: '중립형',
    aggressive: '공격형'
  }
  return types[riskType] || riskType
}

const getRiskTypeDescription = (riskType) => {
  const descriptions = {
    conservative: '원금 손실을 최소화하려는 성향으로, 안정적인 수익을 추구합니다.',
    moderate: '적절한 위험을 감수하며 중위험-중수익을 추구합니다.',
    aggressive: '높은 수익을 위해 적극적인 투자를 선호하며, 위험을 감수할 수 있습니다.'
  }
  return descriptions[riskType] || ''
}

const getQuestionLabel = (key) => {
  const labels = {
    age: '나이',
    gender: '성별',
    income: '연간 소득',
    assets: '총 자산',
    risk_tolerance: '위험 성향',
    financial_knowledge: '금융 지식',
    investment_experience: '투자 경험',
    saving_goal: '저축 목표',
    preferred_term: '선호 투자기간',
    user_type: '직업군'
  }
  return labels[key] || key
}

const getProductTypeDisplay = (type) => {
  const types = {
    deposit: '예금',
    saving: '적금',
    stock: '주식',
    etf: 'ETF',
    goods: '기타 상품'
  }
  return types[type] || type
}

const getProductDescription = (type) => {
  const descriptions = {
    deposit: '안정적인 수익을 제공하는 예금 상품입니다.',
    saving: '정기적인 저축으로 목돈을 마련할 수 있는 적금 상품입니다.',
    stock: '높은 수익을 기대할 수 있는 주식 투자 상품입니다.',
    etf: '분산 투자가 가능한 상장지수펀드입니다.',
    goods: '다양한 투자 상품을 포함한 금융 상품입니다.'
  }
  return descriptions[type] || ''
}

const goToProductPage = (type) => {
  if (!testResult.value.recommendations[type]) return

  const routes = {
    deposit: { name: 'savings' },
    saving: { name: 'savings' },
    stock: { name: 'stocks' },
    etf: { name: 'stocks' },
    goods: { name: 'goods' }
  }

  if (routes[type]) {
    router.push(routes[type])
  }
}

const retakeTest = () => {
  router.push({ name: 'investmenttest' })
}

const goToTest = () => {
  router.push({ name: 'investmenttest' })
}
</script>

<style scoped>
.test-result {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.result-title {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 2rem;
  text-align: center;
}

.result-section {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.result-section h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

/* 투자 성향 섹션 */
.risk-type-content {
  text-align: center;
}

.risk-type-badge {
  display: inline-block;
  padding: 0.5rem 2rem;
  border-radius: 20px;
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.risk-type-badge.conservative {
  background-color: #3498db;
  color: white;
}

.risk-type-badge.moderate {
  background-color: #f1c40f;
  color: white;
}

.risk-type-badge.aggressive {
  background-color: #e74c3c;
  color: white;
}

.risk-type-description {
  color: #666;
  font-size: 1.1rem;
  line-height: 1.6;
}

/* 테스트 응답 섹션 */
.answers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.answer-item {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.answer-label {
  display: block;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.answer-value {
  display: block;
  color: #2c3e50;
  font-weight: bold;
}

/* 추천 상품 섹션 */
.recommendation-items {
  display: grid;
  gap: 1rem;
}

.recommendation-item {
  padding: 1.5rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.recommendation-item.recommended {
  border-color: #3498db;
  background-color: #ebf5fb;
}

.recommendation-item.recommended:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.product-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.product-type {
  font-weight: bold;
  color: #2c3e50;
  font-size: 1.1rem;
}

.recommendation-status {
  color: #666;
}

.recommendation-status.recommended {
  color: #3498db;
}

.product-description {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

/* 버튼 */
.action-buttons {
  text-align: center;
  margin-top: 2rem;
}

.retake-button,
.take-test-button {
  background-color: #3498db;
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 4px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.retake-button:hover,
.take-test-button:hover {
  background-color: #2980b9;
}

.no-result {
  text-align: center;
  padding: 4rem 2rem;
}

.no-result p {
  color: #666;
  margin-bottom: 2rem;
}
</style> 