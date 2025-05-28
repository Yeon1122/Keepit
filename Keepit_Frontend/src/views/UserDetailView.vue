<template>
  <div class="user-detail-container">
    <!-- 로딩 상태 -->
    <div v-if="loading" class="loading-overlay">
      <lottie-player
        :animationData="loadingAnimation"
        :loop="true"
        :autoplay="true"
        style="width: 200px; height: 200px;"
      />
      <p class="loading-text">데이터를 불러오는 중입니다...</p>
    </div>

    <!-- 기존 컨텐츠 -->
    <template v-else>
      <!-- 프로필 섹션 -->
      <div class="profile-card">
        <div class="profile-header">
          <div class="profile-main">
            <div class="profile-image">
              <img src="/images/images_momo/momo_happy.png" alt="프로필 이미지" />
            </div>
            <div class="profile-info">
              <h2 class="user-name">{{ user.nickname }}</h2>
              <p class="user-id">@{{ user.userid }}</p>
              <button v-if="isAuthenticated && !isCurrentUser" @click="toggleFollow"
                :class="['follow-button', { 'following': user.is_following }]">
                <i class="fas" :class="user.is_following ? 'fa-user-check' : 'fa-user-plus'"></i>
                {{ user.is_following ? '팔로잉' : '팔로우' }}
              </button>
            </div>
          </div>
          <div class="profile-stats">
            <div class="stat-item" @click="goToFollow">
              <div class="stat-value">{{ user.following?.length || 0 }}</div>
              <div class="stat-label">팔로우</div>
            </div>
            <div class="stat-item" @click="goToFollow">
              <div class="stat-value">{{ user.followers?.length || 0 }}</div>
              <div class="stat-label">팔로워</div>
            </div>
            <div class="stat-item" @click="goToUserPosts('all')">
              <div class="stat-value">{{ user.posts_summary?.total_posts || 0 }}</div>
              <div class="stat-label">작성글</div>
            </div>
          </div>
        </div>
      </div>

      <div class="content-grid">
        <!-- 투자 성향 분석 카드 -->
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
              <p>{{ user.nickname }}님은 <br>아직 투자 성향 테스트를 하지 않으셨네요!</p>
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
              <button class="filter-button" :class="{ active: selectedFilter === 'all' }" @click="selectedFilter = 'all'">
                전체
              </button>
              <button class="filter-button" :class="{ active: selectedFilter === 'deposit' }"
                @click="selectedFilter = 'deposit'">
                예금
              </button>
              <button class="filter-button" :class="{ active: selectedFilter === 'saving' }"
                @click="selectedFilter = 'saving'">
                적금
              </button>
              <button class="filter-button" :class="{ active: selectedFilter === 'goods' }"
                @click="selectedFilter = 'goods'">
                현물
              </button>
              <button class="filter-button" :class="{ active: selectedFilter === 'stock' }"
                @click="selectedFilter = 'stock'">
                주식
              </button>
              <button class="filter-button" :class="{ active: selectedFilter === 'etf' }" @click="selectedFilter = 'etf'">
                ETF
              </button>
            </div>
          </div>
          <div class="card-content">
            <div v-if="loading" class="loading-state">
              <i class="fas fa-spinner fa-spin"></i>
              <p>상품을 불러오는 중...</p>
            </div>
            <div v-else-if="filteredProducts.length === 0" class="empty-state">
              <i class="fas fa-heart"></i>
              <p>{{ getEmptyStateMessage }}</p>
            </div>
            <div v-else class="products-grid">
              <div v-for="product in limitedFilteredProducts" :key="product.id" class="product-card">
                <div class="product-info">
                  <div class="product-header">
                    <div class="product-type-name">
                      <span class="product-type" :class="product.type">{{ getProductTypeText(product.type) }}</span>
                      <span class="product-title">{{ getProductName(product) }}</span>
                    </div>
                  </div>
                  <!-- 예금/적금 상품일 경우 -->
                  <div v-if="['deposit', 'saving'].includes(product.type)" class="product-details">
                    <div class="detail-item">
                      <span class="label">금리</span>
                      <span class="value">{{ product.interest_rate }}%</span>
                    </div>
                    <div class="detail-item" v-if="product.special_rate">
                      <span class="label">우대금리</span>
                      <span class="value">{{ product.special_rate }}%</span>
                    </div>
                  </div>
                  <!-- 주식/ETF 상품일 경우 -->
                  <div v-else-if="['stock', 'etf'].includes(product.type)" class="product-details">
                    <div class="detail-item">
                      <span class="label">현재가</span>
                      <span class="value">{{ formatPrice(product.current_price) }}원</span>
                    </div>
                    <div class="detail-item">
                      <span class="label">변동가</span>
                      <span class="value" :class="getPriceChangeClass(product.price_change)">
                        <i :class="['fas', product.price_change > 0 ? 'fa-caret-up' : 'fa-caret-down']"></i>
                        {{ formatPriceChange(product.price_change) }}원
                      </span>
                    </div>
                  </div>
                  <!-- 현물 상품일 경우 -->
                  <div v-else-if="product.type === 'goods'" class="product-details">
                    <div class="detail-item">
                      <span class="label">현재가</span>
                      <span class="value">{{ formatPrice(product.current_price) }} {{ product.unit }}</span>
                    </div>
                    <div class="detail-item">
                      <span class="label">변동가</span>
                      <span class="value" :class="getPriceChangeClass(product.price_change)">
                        <i :class="['fas', product.price_change > 0 ? 'fa-caret-up' : 'fa-caret-down']"></i>
                        {{ formatPriceChange(product.price_change) }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              <div v-if="filteredProducts.length > 1" class="view-more-section">
                <button class="view-more-button" @click="goToFavorites">
                  더보기
                  <i class="fas fa-chevron-right"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 작성 글 카드 -->
        <div class="content-card">
          <div class="card-header">
            <h3>최근 작성글</h3>
            <button class="action-button" @click="goToUserPosts('all')">전체보기</button>
          </div>
          <div class="card-content">
            <div class="posts-grid">
              <!-- 자유 게시판 -->
              <div class="posts-section">
                <h4>자유게시판</h4>
                <ul class="posts-list">
                  <li v-for="post in freePosts.slice(0, 2)" :key="post.id" @click="goToPost('free', post.id)"
                    class="post-item">
                    <div class="post-title">{{ post.title }}</div>
                    <div class="post-meta">
                      <span class="post-date">{{ formatDate(post.created_at) }}</span>
                      <div class="post-stats">
                        <span class="likes">
                          <i class="fas fa-thumbs-up"></i> {{ post.likes_count }}
                        </span>
                        <span class="comments">
                          <i class="fas fa-comment"></i> {{ post.comments.length }}
                        </span>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>

              <!-- 질문 게시판 -->
              <div class="posts-section">
                <h4>질문게시판</h4>
                <ul class="posts-list">
                  <li v-for="post in questionPosts.slice(0, 2)" :key="post.id" @click="goToPost('question', post.id)"
                    class="post-item">
                    <div class="post-title">
                      {{ post.title }}
                      <span v-if="post.is_solved" class="solved-badge">해결</span>
                    </div>
                    <div class="post-meta">
                      <span class="post-date">{{ formatDate(post.created_at) }}</span>
                      <div class="post-stats">
                        <span class="likes">
                          <i class="fas fa-thumbs-up"></i> {{ post.likes_count }}
                        </span>
                        <span class="comments">
                          <i class="fas fa-comment"></i> {{ post.comments.length }}
                        </span>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/users.js'
import loadingAnimation from '@/assets/animations/loading.json'
import LottiePlayer from '@/components/LottiePlayer.vue'

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

const loading = ref(true)
const likedProducts = ref([])
const selectedFilter = ref('all')
const freePosts = ref([])
const questionPosts = ref([])

const isAuthenticated = computed(() => accountStore.isAuthenticated)
const isCurrentUser = computed(() => user.value.userid === accountStore.userId)

const filterTypes = [
  { label: '전체', value: 'all' },
  { label: '예금', value: 'deposit' },
  { label: '적금', value: 'saving' },
  { label: '현물', value: 'goods' },
  { label: '주식', value: 'stock' },
  { label: 'ETF', value: 'etf' },
]

const filteredProducts = computed(() => {
  if (selectedFilter.value === 'all') {
    return likedProducts.value
  }
  return likedProducts.value.filter(product => product.type === selectedFilter.value)
})

const limitedFilteredProducts = computed(() => {
  return filteredProducts.value.slice(0, 1)
})

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
  if (selectedFilter.value === 'all') {
    return `${user.value.nickname}님이 찜한 상품이 없습니다.`
  }
  const typeMap = {
    deposit: '예금',
    saving: '적금',
    stock: '주식',
    etf: 'ETF',
    goods: '현물'
  }
  return `찜한 ${typeMap[selectedFilter.value]} 상품이 없습니다.`
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
  router.push({ name: 'favorites', query: { userid: user.value.userid } })
}

const goToSavings = () => {
  router.push({ name: 'savings' })
}

const goToUserPosts = (type) => {
  router.push({
    name: 'myposts',
    query: {
      userid: user.value.userid,
      type: type
    }
  })
}

const goToFollow = () => {
  router.push({
    name: 'follow',
    params: { userid: user.value.userid }
  })
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
      url: `/api/v1/users/${user.value.userid}/follow/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })

    if (response.data.data) {
      user.value.is_following = response.data.data.is_following
      user.value.followers = response.data.data.followers
      user.value.following = response.data.data.following
    }
  } catch (err) {
    console.error('팔로우 토글 실패:', err)
    if (err.response?.data?.message) {
      alert(err.response.data.message)
    } else {
      alert('팔로우 처리에 실패했습니다.')
    }
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

  // 현재 접근하는 userid가 로그인한 사용자의 userid와 같은 경우 마이페이지로 리다이렉트
  if (userId === accountStore.userId) {
    console.log('본인 페이지 접근 감지 - 마이페이지로 리다이렉트')
    router.push({ name: 'mypage' })
    return
  }

  try {
    const userRes = await axios.get(`/api/v1/users/${userId}/`, {
      headers: { Authorization: `Token ${token}` }
    })

    if (!userRes.data || !userRes.data.userid) {
      throw new Error('유효하지 않은 사용자 데이터')
    }

    const favoritesRes = await axios.get(`/api/v1/users/favorites/${userId}/`, {
      headers: { Authorization: `Token ${token}` }
    })

    // 최근 게시글 가져오기
    const postsRes = await axios.get(`/api/v1/community/user-posts/${userId}/`, {
      headers: { Authorization: `Token ${token}` }
    })

    user.value = {
      ...userRes.data,
      test_result: null,
      liked_products: favoritesRes.data
    }

    // 게시글 분류
    if (postsRes.data && postsRes.data.posts) {
      freePosts.value = postsRes.data.posts.filter(post => post.board_type === 'free')
      questionPosts.value = postsRes.data.posts.filter(post => post.board_type === 'question')
    }

    try {
      const testRes = await axios.get(`/api/v1/test/result/${userId}/`, {
        headers: { Authorization: `Token ${token}` }
      })
      user.value.test_result = testRes.data
    } catch (e) {
      if (e.response?.status === 404) user.value.test_result = null
    }

    likedProducts.value = favoritesRes.data
    loading.value = false
  } catch (err) {
    console.error('사용자 정보 로딩 실패:', err)
    if (err.response?.status === 401) {
      alert('로그인이 필요합니다.')
      router.push({ name: 'login' })
    } else if (err.response?.status === 404) {
      alert('존재하지 않는 사용자입니다.')
      router.push({ name: 'home' })
    } else {
      alert('사용자 정보를 불러오지 못했습니다.')
    }
    loading.value = false
  }
})

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
}

const goToPost = (type, postId) => {
  router.push({
    name: type === 'free' ? 'freepostdetail' : 'questionpostdetail',
    params: { postId }
  })
}
</script>

<style scoped>
.user-detail-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
  font-family: 'Pretendard', sans-serif;
}

.profile-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
}

.profile-main {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.profile-image {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  background: #f0f0f0;
  border: 4px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.profile-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.user-name {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
  color: #333;
}

.user-id {
  font-size: 1rem;
  color: #666;
  margin: 0;
}

.follow-button {
  align-self: flex-start;
  padding: 0.6rem 1.2rem;
  border-radius: 999px;
  font-size: 0.95rem;
  font-weight: 600;
  border: 2px solid #145c2b;
  background: white;
  color: #145c2b;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.follow-button i {
  font-size: 0.9rem;
}

.follow-button:hover {
  background: #f1f9f3;
}

.follow-button.following {
  background: #145c2b;
  color: white;
}

.follow-button.following:hover {
  background: #0d4420;
  border-color: #0d4420;
}

.profile-stats {
  display: flex;
  gap: 2rem;
  margin-left: auto;
}

.stat-item {
  text-align: center;
  cursor: pointer;
  padding: 0.5rem 1rem;
  min-width: 100px;
  transition: transform 0.2s;
}

.stat-item:hover {
  transform: translateY(-2px);
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #145c2b;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.2rem;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}

.content-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  min-height: 320px;
  display: flex;
  flex-direction: column;
}

.content-card:last-child {
  grid-column: 1 / -1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.card-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.25rem;
}

.card-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.test-result {
  width: 100%;
  text-align: center;
  padding: 2rem;
  background: #fff;
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

.empty-state {
  width: 100%;
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

.products-grid {
  width: 100%;
  display: grid;
  gap: 1rem;
}

.product-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.2rem;
  cursor: pointer;
  transition: all 0.2s;
}

.product-card:hover {
  background: #f1f9f3;
  transform: translateX(4px);
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-type-name {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.product-type {
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 500;
  color: white;
  background-color: #145c2b;
  white-space: nowrap;
}

.product-title {
  font-size: 1.1rem;
  color: #333;
  font-weight: 500;
}

.product-details {
  margin-top: 0.8rem;
  display: grid;
  gap: 0.4rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  color: #666;
  font-size: 0.9rem;
}

.value {
  font-weight: 500;
  color: #333;
}

.value.up {
  color: #d63031;
  display: flex;
  align-items: center;
  gap: 0.2rem;
}

.value.down {
  color: #0984e3;
  display: flex;
  align-items: center;
  gap: 0.2rem;
}

.posts-grid {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}

.posts-section {
  margin-bottom: 2rem;
}

.posts-section h4 {
  font-size: 1rem;
  color: #495057;
  margin-bottom: 1rem;
}

.posts-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.post-item {
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.post-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.post-title {
  font-size: 1rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  color: #666;
}

.post-date {
  color: #666;
}

.post-stats {
  display: flex;
  gap: 1rem;
}

.likes,
.comments {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.likes i {
  color: #e74c3c;
}

.comments i {
  color: #145c2b;
}

.solved-badge {
  background: #145c2b;
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  margin-left: 0.5rem;
}

.filter-section {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #eee;
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.filter-button {
  padding: 0.4rem 1rem;
  border: 1px solid #dee2e6;
  border-radius: 20px;
  background: white;
  color: #495057;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.filter-button:hover {
  background: #f8f9fa;
}

.filter-button.active {
  background: #145c2b;
  color: white;
  border-color: #145c2b;
}

.view-more-section {
  text-align: center;
  margin-top: 1rem;
}

.view-more-button {
  padding: 0.6rem 1rem;
  border: 1px solid #145c2b;
  border-radius: 4px;
  background: none;
  color: #145c2b;
  cursor: pointer;
  transition: all 0.2s;
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
  }

  .profile-stats {
    width: 100%;
    justify-content: space-around;
    margin-top: 1.5rem;
    margin-left: 0;
  }

  .stat-item {
    min-width: auto;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .content-card:last-child {
    grid-column: auto;
  }

  .posts-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .profile-main {
    flex-direction: column;
    text-align: center;
  }

  .profile-info {
    align-items: center;
  }

  .follow-button {
    align-self: center;
  }
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-text {
  margin-top: 1rem;
  font-size: 1.1rem;
  color: #666;
}
</style>
