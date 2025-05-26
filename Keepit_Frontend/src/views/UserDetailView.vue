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
            <button 
              v-if="isAuthenticated && user.userid !== currentUser.userid"
              @click="toggleFollow"
              :class="['follow-button', { 'following': user.is_following }]"
            >
              {{ user.is_following ? '팔로잉' : '팔로우' }}
            </button>
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

    <div class="content-grid">
      <!-- 투자 성향 분석 -->
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
        </div>
        <div class="filter-section">
          <div class="filter-buttons">
            <button v-for="type in filterTypes" :key="type.value"
              class="filter-button"
              :class="{ active: selectedFilter === type.value }"
              @click="selectedFilter = type.value">
              {{ type.label }}
            </button>
          </div>
        </div>
        <div class="card-content">
          <template v-if="limitedFilteredProducts.length">
            <div class="product-card" v-for="product in limitedFilteredProducts" :key="product.id">
              <div class="product-info">
                <div class="product-header">
                  <div class="product-type-name">
                    <span class="product-type" :class="product.type">
                      {{ getProductTypeText(product.type) }}
                    </span>
                    <span class="product-title">{{ getProductName(product) }}</span>
                  </div>
                </div>
                <div v-if="['deposit', 'saving'].includes(product.type)" class="product-details">
                  <div class="rate-info">
                    <span class="label">금리</span>
                    <span class="value">{{ product.interest_rate }}% ~ {{ product.special_rate }}%</span>
                  </div>
                  <div class="term-info">
                    <span class="label">기간</span>
                    <span class="value">{{ product.term }}개월</span>
                  </div>
                </div>
                <div v-else-if="['stock', 'etf'].includes(product.type)" class="product-details">
                  <div class="price-info">
                    <span class="label">현재가</span>
                    <span class="value">{{ formatPrice(product.current_price) }}원</span>
                  </div>
                  <div class="change-info">
                    <span class="label">변동가</span>
                    <span class="value" :class="getPriceChangeClass(product.price_change)">
                      <i :class="['fas', product.price_change > 0 ? 'fa-caret-up' : 'fa-caret-down']"></i>
                      {{ formatPriceChange(product.price_change) }}원
                    </span>
                  </div>
                </div>
                <div v-else-if="product.type === 'goods'" class="product-details">
                  <div class="price-info">
                    <span class="label">현재가</span>
                    <span class="value">${{ formatPrice(product.current_price) }} / oz</span>
                  </div>
                  <div class="change-info">
                    <span class="label">변동가</span>
                    <span class="value" :class="getPriceChangeClass(product.price_change)">
                      <i :class="['fas', product.price_change > 0 ? 'fa-caret-up' : 'fa-caret-down']"></i>
                      ${{ formatPriceChange(product.price_change) }}
                    </span>
                  </div>
                </div>
              </div>
              <div class="product-divider"></div>
            </div>
            <div v-if="filteredProducts.length > 3" class="view-more-section">
              <button class="view-more-button" @click="goToFavorites">
                더보기
                <i class="fas fa-chevron-right"></i>
              </button>
            </div>
          </template>
          <div v-else class="empty-state">
            <i class="fas fa-heart"></i>
            <p>{{ getEmptyStateMessage }}</p>
            <p class="sub-text">마음에 드는 상품을 찜해보세요!</p>
            <button class="action-button primary" @click="goToSavings">
              상품 보러가기
              <i class="fas fa-arrow-right"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
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
  liked_products: [],
  followers: [],
  following: [],
  posts_summary: {}
})

const selectedFilter = ref('all')

const isAuthenticated = computed(() => accountStore.isAuthenticated)
const currentUser = computed(() => accountStore.user)

const filterTypes = [
  { label: '전체', value: 'all' },
  { label: '예금', value: 'deposit' },
  { label: '적금', value: 'saving' },
  { label: '현물', value: 'goods' },
  { label: '주식', value: 'stock' },
  { label: 'ETF', value: 'etf' },
]

const filteredProducts = computed(() => {
  if (selectedFilter.value === 'all') return user.value.liked_products || []
  return (user.value.liked_products || []).filter(p => p.type === selectedFilter.value)
})

const limitedFilteredProducts = computed(() => filteredProducts.value.slice(0, 3))

const getProductName = (product) => product.name || '이름 없음'

const getProductTypeText = (type) => {
  const map = {
    deposit: '정기예금',
    saving: '적금',
    stock: '주식',
    etf: 'ETF',
    goods: '현물'
  }
  return map[type] || type
}

const formatPrice = (val) => Number(val).toLocaleString()
const formatPriceChange = (val) => Math.abs(Number(val)).toLocaleString()
const getPriceChangeClass = (val) => val > 0 ? 'up' : val < 0 ? 'down' : 'neutral'

const getEmptyStateMessage = computed(() => {
  if (selectedFilter.value === 'all') return '아직 찜한 상품이 없습니다.'
  return `${getProductTypeText(selectedFilter.value)} 찜한 상품이 없습니다.`
})

const getRiskTypeDisplay = (type) => ({
  conservative: '안정형',
  moderate: '중립형',
  aggressive: '공격형'
})[type] || type

const getRiskTypeDescription = (type) => ({
  conservative: '원금 손실을 최소화하려는 성향으로, 안정적인 수익을 추구합니다.',
  moderate: '적절한 위험을 감수하며 중위험-중수익을 추구합니다.',
  aggressive: '높은 수익을 위해 적극적인 투자를 선호합니다.'
})[type] || ''

const goToFavorites = () => {
  router.push({ name: 'favorites', query: { userid: route.params.userid } })
}

const goToSavings = () => {
  router.push({ name: 'savings' })
}

const toggleFollow = async () => {
  if (!isAuthenticated.value) {
    alert('로그인이 필요한 서비스입니다.')
    router.push({ name: 'login' })
    return
  }

  try {
    const method = user.value.is_following ? 'DELETE' : 'POST'
    const response = await axios({
      method,
      url: `http://127.0.0.1:8000/api/v1/users/follow/${user.value.userid}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })

    // 팔로우 상태 및 카운트 업데이트
    user.value.is_following = response.data.data.is_following
    user.value.followers = response.data.data.followers
    user.value.following = response.data.data.following
  } catch (err) {
    console.error('팔로우 토글 실패:', err)
    alert('팔로우 처리에 실패했습니다.')
  }
}

onMounted(async () => {
  const userId = route.params.userid
  const token = accountStore.token

  if (!token) {
    alert('로그인이 필요한 서비스입니다.')
    router.push({ name: 'login' })
    return
  }

  try {
    const userRes = await axios.get(`/api/v1/users/${userId}/`, {
      headers: { Authorization: `Token ${token}` }
    })

    const favoritesRes = await axios.get(`/api/v1/products/favorites/${userId}/`, {
      headers: { Authorization: `Token ${token}` }
    })

    user.value = {
      ...userRes.data,
      test_result: null,
      liked_products: favoritesRes.data
    }

    try {
      const testRes = await axios.get(`/api/v1/test/result/${userId}/`, {
        headers: { Authorization: `Token ${token}` }
      })
      user.value.test_result = testRes.data
    } catch (e) {
      if (e.response?.status === 404) user.value.test_result = null
    }
  } catch (err) {
    if (err.response?.status === 401) {
      alert('로그인이 필요합니다.')
      router.push({ name: 'login' })
    } else if (err.response?.status === 404) {
      alert('존재하지 않는 사용자입니다.')
      router.push({ name: 'home' })
    } else {
      alert('사용자 정보를 불러오지 못했습니다.')
    }
  }
})
</script>

<style scoped>
.user-detail-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
  font-family: 'Pretendard', sans-serif;
}

/* 카드 공통 */
.content-card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.card-header {
  padding: 1.2rem 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  font-size: 1.2rem;
  color: #333;
  margin: 0;
}

.card-content {
  padding: 1.5rem;
}

/* 프로필 섹션 */
.profile-info {
  text-align: center;
}

.profile-header {
  margin-bottom: 1.5rem;
}

.nickname {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #333;
}

.userid {
  font-size: 1rem;
  color: #888;
}

.profile-stats {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin: 1rem 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
  padding: 1rem 0;
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #145c2b;
}

/* 게시글 요약 */
.post-stats {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.post-stat {
  display: flex;
  justify-content: space-between;
  background: #f9f9f9;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
}

.post-type {
  color: #444;
}

.post-count {
  font-weight: 600;
  color: #145c2b;
}

/* 투자 성향 */
.test-result {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
}

.risk-type-badge {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  border-radius: 999px;
  font-size: 1.1rem;
  font-weight: bold;
  color: white;
  margin-bottom: 1rem;
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
  font-size: 0.95rem;
  line-height: 1.5;
}

/* 찜한 상품 필터 */
.filter-section {
  border-bottom: 1px solid #eee;
  padding: 1rem 1.5rem;
}

.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.filter-button {
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  border: 1px solid #ccc;
  background: white;
  color: #444;
  cursor: pointer;
  transition: 0.2s;
}

.filter-button:hover {
  background: #f2f2f2;
}

.filter-button.active {
  background: #145c2b;
  color: white;
  border-color: #145c2b;
}

/* 찜한 상품 */
.product-card {
  padding: 1rem 0;
  border-bottom: 1px solid #eee;
}

.product-card:last-child {
  border-bottom: none;
}

.product-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.product-type {
  font-size: 0.85rem;
  background-color: #145c2b;
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
}

.product-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.product-details {
  margin-top: 0.5rem;
  display: grid;
  gap: 0.4rem;
  font-size: 0.9rem;
}

.label {
  color: #666;
}

.value {
  font-weight: 500;
  color: #333;
}

.price-up {
  color: #e74c3c;
}

.price-down {
  color: #3498db;
}

.product-divider {
  margin-top: 1rem;
  height: 1px;
  background-color: #eee;
}

/* 비어있는 상태 */
.empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.empty-state i {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #145c2b;
}

.empty-state p {
  font-size: 1.1rem;
  margin: 0.3rem 0;
  color: #333;
}

.empty-state .sub-text {
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

/* 버튼 */
.action-button {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  border: 1px solid #ccc;
  background-color: white;
  color: #145c2b;
  cursor: pointer;
  transition: 0.2s;
}

.action-button:hover {
  background-color: #f1f3f5;
}

.action-button.primary {
  background-color: #145c2b;
  color: white;
  border-color: #145c2b;
}

.action-button.primary:hover {
  background-color: #0d4420;
}

/* 더보기 버튼 */
.view-more-section {
  text-align: center;
  margin-top: 1rem;
}

.view-more-button {
  background: none;
  border: none;
  color: #145c2b;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.95rem;
}

/* 반응형 */
@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .profile-stats {
    flex-direction: column;
    gap: 1rem;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style>


