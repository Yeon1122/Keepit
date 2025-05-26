<template>
  <div class="user-detail-container">
    <!-- 프로필 정보 카드 -->
    <div class="content-card">
      <div class="card-header">
        <h3>프로필 정보</h3>
      </div>
      <div class="card-content">
        <div class="profile-info">
          <div class="profile-header">
            <h2 class="nickname">{{ user.nickname }}</h2>
            <span class="userid">@{{ user.userid }}</span>
          </div>
          <div class="profile-stats">
            <div class="stat-item">
              <span class="stat-label">팔로워</span>
              <span class="stat-value">{{ user.followers?.length || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">팔로잉</span>
              <span class="stat-value">{{ user.following?.length || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">게시글</span>
              <span class="stat-value">{{ user.posts_summary?.total_posts || 0 }}</span>
            </div>
          </div>
          <div class="post-stats">
            <div class="post-stat">
              <span class="post-type">자유게시판</span>
              <span class="post-count">{{ user.posts_summary?.free_posts || 0 }}개</span>
            </div>
            <div class="post-stat">
              <span class="post-type">질문게시판</span>
              <span class="post-count">{{ user.posts_summary?.question_posts || 0 }}개</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 성향 테스트 결과 카드 -->
    <div class="content-card">
      <div class="card-header">
        <h3>투자 성향 분석</h3>
      </div>
      <div class="card-content">
        <template v-if="user.test_result">
          <div class="test-result">
            <div class="risk-type-content">
              <div class="risk-type-badge" :class="user.test_result.risk_type">
                {{ getRiskTypeDisplay(user.test_result.risk_type) }}
              </div>
              <p class="risk-type-description">
                {{ getRiskTypeDescription(user.test_result.risk_type) }}
              </p>
            </div>
            <div class="recommendations-preview">
              <h4>추천 투자 상품</h4>
              <div class="recommendation-chips">
                <div 
                  v-for="(isRecommended, type) in user.test_result.recommendations" 
                  :key="type"
                  class="recommendation-chip"
                  :class="{ 'recommended': isRecommended }"
                >
                  {{ getProductTypeDisplay(type) }}
                </div>
              </div>
            </div>
          </div>
        </template>
        <div v-else class="empty-state">
          <i class="fas fa-chart-line"></i>
          <p>{{ user.nickname }}님은 아직 투자 성향 테스트를 하지 않으셨네요!</p>
        </div>
      </div>
    </div>

    <!-- 찜한 상품 카드 -->
    <div class="content-card">
      <div class="card-header">
        <h3>찜한 상품</h3>
        <button v-if="user.liked_products?.length" class="action-button" @click="goToSavings">
          전체보기
        </button>
      </div>
      <div class="card-content">
        <template v-if="user.liked_products?.length">
          <ul class="product-list">
            <li v-for="product in user.liked_products" :key="product.id" class="product-item">
              <div class="product-info-header">
                <span class="product-type">{{ product.type === 'deposit' ? '정기예금' : '적금' }}</span>
                <span class="bank-name">{{ product.company }}</span>
              </div>
              <div class="product-name">{{ product.name }}</div>
              <div class="product-details">
                <div class="rate-info">
                  <span class="label">금리</span>
                  <span class="value">{{ product.interest_rate }}% ~ {{ product.special_rate }}%</span>
                </div>
                <div class="term-info">
                  <span class="label">기간</span>
                  <span class="value">{{ product.term }}개월</span>
                </div>
              </div>
            </li>
          </ul>
        </template>
        <div v-else class="empty-state">
          <i class="fas fa-heart"></i>
          <p>아직 찜한 상품이 없습니다.</p>
          <p class="sub-text">{{ user.nickname }}님이 아직 찜한 상품이 없습니다.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/users.js'

const router = useRouter()
const route = useRoute()
const accountStore = useAccountStore()

const user = ref({
  userid: '',
  nickname: '',
  test_result: null,
  liked_products: []
})

onMounted(async () => {
  const userId = route.params.userid
  const token = accountStore.token

  if (!token) {
    alert('로그인이 필요한 서비스입니다.')
    router.push({ name: 'login' })
    return
  }

  try {
    // 사용자 정보 가져오기
    const userRes = await axios.get(`/api/v1/users/${userId}/`, {
      headers: {
        Authorization: `Token ${token}`
      }
    })

    // 찜한 상품 목록 가져오기
    const favoritesRes = await axios.get(`/api/v1/products/favorites/${userId}/`, {
      headers: {
        Authorization: `Token ${token}`
      }
    })

    // 기본 사용자 정보 설정
    user.value = {
      ...userRes.data,
      test_result: null,
      liked_products: favoritesRes.data
    }

    console.log('사용자 정보:', userRes.data)

    // 투자성향 테스트 결과 가져오기
    try {
      console.log('테스트 결과 요청 URL:', `/api/v1/test/result/${userId}/`)
      const testRes = await axios.get(`/api/v1/test/result/${userId}/`, {
        headers: {
          Authorization: `Token ${token}`
        }
      })
      console.log('테스트 결과 응답:', testRes.data)
      user.value.test_result = testRes.data
    } catch (testErr) {
      console.error('테스트 결과 로딩 실패:', testErr.response || testErr)
      if (testErr.response?.status === 404) {
        console.log('테스트 결과 없음 - userId:', userId)
        user.value.test_result = null
      }
    }

  } catch (err) {
    console.error('사용자 정보 로딩 실패:', err)
    if (err.response?.status === 401) {
      alert('로그인이 필요한 서비스입니다.')
      router.push({ name: 'login' })
    } else if (err.response?.status === 404) {
      alert('존재하지 않는 사용자입니다.')
      router.push({ name: 'home' })
    } else {
      alert('사용자 정보를 불러오는데 실패했습니다.')
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
    conservative: '원금 손실을 최소화하려는 성향으로, 안정적인 수익을 추구합니다. 예적금 중심의 투자를 선호하며, 위험을 최소화하려 합니다.',
    moderate: '적절한 위험을 감수하며 중위험-중수익을 추구합니다. 안정성과 수익성의 균형을 맞추려 하며, 분산 투자를 선호합니다.',
    aggressive: '높은 수익을 위해 적극적인 투자를 선호하며, 위험을 감수할 수 있습니다. 주식이나 고위험 상품에 투자하는 것을 고려합니다.'
  }
  return descriptions[riskType] || ''
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

const goToSavings = () => {
  router.push({ 
    name: 'savings',
    query: {
      userId: route.params.userid,
      nickname: user.value.nickname
    }
  })
}
</script>

<style scoped>
.user-detail-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.content-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

.action-button {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: 1px solid #dee2e6;
  background: white;
  color: #495057;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.action-button:hover {
  background: #e9ecef;
}

.card-content {
  padding: 1.5rem;
}

.product-info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.product-type {
  font-size: 0.8rem;
  padding: 0.2rem 0.5rem;
  background-color: #e3f2fd;
  color: #1976d2;
  border-radius: 4px;
}

.bank-name {
  font-size: 0.9rem;
  color: #666;
}

.product-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.product-details {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
}

.rate-info, .term-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.label {
  color: #666;
}

.value {
  font-weight: 500;
  color: #333;
}

.rate-info .value {
  color: #e64545;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.empty-state i {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #145c2b;
}

.empty-state p {
  margin: 0.5rem 0;
  font-size: 1.1rem;
  color: #333;
}

.empty-state .sub-text {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 1.5rem;
}

.product-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.product-item {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.product-item:last-child {
  border-bottom: none;
}

.test-result {
  text-align: center;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.risk-type-content {
  text-align: center;
  margin-bottom: 1.5rem;
}

.risk-type-badge {
  display: inline-block;
  padding: 0.5rem 2rem;
  border-radius: 20px;
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: white;
}

.risk-type-badge.conservative {
  background-color: #3498db;
}

.risk-type-badge.moderate {
  background-color: #f1c40f;
}

.risk-type-badge.aggressive {
  background-color: #e74c3c;
}

.risk-type-description {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
}

.recommendations-preview {
  margin-top: 1.5rem;
}

.recommendations-preview h4 {
  color: #2c3e50;
  font-size: 1rem;
  margin-bottom: 1rem;
}

.recommendation-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}

.recommendation-chip {
  padding: 0.3rem 1rem;
  border-radius: 15px;
  font-size: 0.9rem;
  background-color: #f8f9fa;
  color: #666;
  border: 1px solid #ddd;
}

.recommendation-chip.recommended {
  background-color: #ebf5fb;
  border-color: #3498db;
  color: #3498db;
}

.profile-info {
  padding: 1rem;
}

.profile-header {
  margin-bottom: 1.5rem;
  text-align: center;
}

.nickname {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.userid {
  font-size: 1rem;
  color: #666;
}

.profile-stats {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 1.5rem;
  padding: 1rem 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
}

.post-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.post-stat {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.post-type {
  color: #495057;
}

.post-count {
  font-weight: 500;
  color: #333;
}
</style> 