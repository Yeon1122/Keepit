<template>
  <div class="mypage-container">
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
            <button 
              @click="handleFollowAction" 
              class="follow-button"
              :class="{ 'is-following': isFollowing }">
              {{ isFollowing ? '팔로잉 중' : '팔로우하기' }}
            </button>
          </div>
        </div>
        <div class="profile-stats">
          <div class="stat-item" @click="goToFollow">
            <div class="stat-value">{{ user.following?.length ?? 0 }}</div>
            <div class="stat-label">팔로우</div>
          </div>
          <div class="stat-item" @click="goToFollow">
            <div class="stat-value">{{ user.followers?.length ?? 0 }}</div>
            <div class="stat-label">팔로워</div>
          </div>
          <div class="stat-item" @click="goToUserPosts">
            <div class="stat-value">{{ user.posts_summary?.total_posts ?? 0 }}</div>
            <div class="stat-label">작성글</div>
          </div>
        </div>
      </div>
    </div>

    <div class="content-grid">
      <!-- 성향 테스트 결과 카드 -->
      <div class="content-card">
        <div class="card-header">
          <h3>투자 성향 분석</h3>
        </div>
        <div class="card-content">
          <template v-if="user.test_result">
            <div class="test-result">
              <div class="result-header">
                <div class="result-type-text">{{ user.nickname }}님은</div>
                <div class="result-type">{{ user.test_result.type }}</div>
              </div>
              <div class="result-score">총점: {{ user.test_result.total_score }}점</div>
            </div>
          </template>
          <div v-else class="empty-state">
            <i class="fas fa-chart-line"></i>
            <p>아직 투자 성향 테스트를 진행하지 않았습니다.</p>
          </div>
        </div>
      </div>

      <!-- 찜한 상품 카드 -->
      <div class="content-card">
        <div class="card-header">
          <h3>찜한 상품</h3>
        </div>
        <div class="filter-section">
          <div class="filter-buttons filter-align">
            <button 
              class="filter-button" 
              :class="{ active: selectedFilter === 'all' }"
              @click="selectedFilter = 'all'"
            >
              전체
            </button>
            <button 
              class="filter-button" 
              :class="{ active: selectedFilter === 'deposit' }"
              @click="selectedFilter = 'deposit'"
            >
              예금
            </button>
            <button 
              class="filter-button" 
              :class="{ active: selectedFilter === 'saving' }"
              @click="selectedFilter = 'saving'"
            >
              적금
            </button>
            <button 
              class="filter-button" 
              :class="{ active: selectedFilter === 'goods' }"
              @click="selectedFilter = 'goods'"
            >
              현물
            </button>
            <button 
              class="filter-button" 
              :class="{ active: selectedFilter === 'stock' }"
              @click="selectedFilter = 'stock'"
            >
              주식
            </button>
            <button 
              class="filter-button" 
              :class="{ active: selectedFilter === 'etf' }"
              @click="selectedFilter = 'etf'"
            >
              ETF
            </button>
          </div>
        </div>
        <div class="card-content">
          <template v-if="limitedFilteredProducts.length">
            <div class="product-card" v-for="product in limitedFilteredProducts" :key="product.id" @click="goToProductDetail(product)" style="cursor:pointer;">
              <div class="product-info">
                <div class="product-header">
                  <div class="product-type-name">
                    <span class="product-type" :class="product.type">{{ getProductTypeText(product.type) }}</span>
                    <span class="product-title">{{ getProductName(product) }}</span>
                  </div>
                </div>
                <!-- 예금/적금 상품일 경우 -->
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
                <!-- 주식/ETF 상품일 경우 -->
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
                <!-- 현물 상품일 경우 -->
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
          </template>
          <div v-else class="empty-state">
            <i class="fas fa-heart"></i>
            <p>{{ getEmptyStateMessage }}</p>
          </div>
        </div>
      </div>

      <!-- 작성 글 카드 -->
      <div class="content-card">
        <div class="card-header">
          <h3>최근 작성글</h3>
        </div>
        <div class="card-content">
          <div v-if="freePosts.length || questionPosts.length">
            <div class="posts-grid">
              <!-- 자유 게시판 -->
              <div v-if="freePosts.length" class="posts-section">
                <h4>자유게시판</h4>
                <ul class="posts-list">
                  <li v-for="post in freePosts.slice(0, 3)" :key="post.id" 
                      @click="goToPost('free', post.id)" 
                      class="post-item">
                    <div class="post-title">{{ post.title }}</div>
                    <div class="post-meta">
                      <span class="post-date">{{ formatDate(post.created_at) }}</span>
                    </div>
                  </li>
                </ul>
              </div>

              <!-- 질문 게시판 -->
              <div v-if="questionPosts.length" class="posts-section">
                <h4>질문게시판</h4>
                <ul class="posts-list">
                  <li v-for="post in questionPosts.slice(0, 3)" :key="post.id" 
                      @click="goToPost('question', post.id)"
                      class="post-item">
                    <div class="post-title">
                      {{ post.title }}
                      <span v-if="post.is_solved" class="solved-badge">해결</span>
                    </div>
                    <div class="post-meta">
                      <span class="post-date">{{ formatDate(post.created_at) }}</span>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div v-else class="empty-state">
            <i class="fas fa-pen"></i>
            <p>작성한 게시글이 없습니다.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios, { AxiosError } from 'axios'
import { useAccountStore } from '@/stores/users.js'
import { useRoute, useRouter } from 'vue-router'

const accountStore = useAccountStore()
const route = useRoute()
const router = useRouter()

const user = ref({
  userid: '',
  nickname: '',
  followers: [],
  following: [],
  test_result: null,
  posts_summary: {
    total_posts: 0,
    free_posts: 0,
    question_posts: 0
  },
  recent_posts: [],
  liked_products: []
})

const freePosts = ref([])
const questionPosts = ref([])
const isFollowing = ref(false)
const selectedFilter = ref('all')

// 필터링된 상품 목록을 계산하는 computed 속성
const filteredProducts = computed(() => {
  const products = user.value.liked_products || []
  if (selectedFilter.value === 'all') {
    return products
  }
  return products.filter(product => product.type === selectedFilter.value)
})

// 필터링된 상품 목록에서 최대 4개만 보여주는 computed 속성
const limitedFilteredProducts = computed(() => {
  return filteredProducts.value.slice(0, 4)
})

// 빈 상태 메시지를 동적으로 생성하는 computed 속성
const getEmptyStateMessage = computed(() => {
  if (selectedFilter.value === 'all') {
    return '찜한 상품이 없습니다.'
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

// 상품 타입 텍스트 변환 함수
const getProductTypeText = (type) => {
  const typeMap = {
    deposit: '예금',
    saving: '적금',
    stock: '주식',
    etf: 'ETF',
    goods: '현물'
  }
  return typeMap[type] || type
}

// 상품명 가져오는 함수
const getProductName = (product) => {
  return product.name
}

// 가격 포맷팅 함수
const formatPrice = (price) => {
  if (!price) return '0'
  return price.toLocaleString()
}

// 가격 변동 포맷팅 함수
const formatPriceChange = (change) => {
  if (!change) return '0'
  return Math.abs(change).toLocaleString()
}

// 가격 변동에 따른 클래스 반환 함수
const getPriceChangeClass = (change) => {
  if (!change) return ''
  return change > 0 ? 'price-up' : 'price-down'
}

onMounted(async () => {
  const token = accountStore.token
  if (!token) {
    alert('⚠️ 로그인이 필요한 서비스입니다.')
    router.push({ name: 'login' })
    return
  }

  // 자신의 프로필 페이지 접근 시 마이페이지로 리다이렉트
  if (route.params.userid === accountStore.userId) {
    router.push({ name: 'mypage' })
    return
  }

  try {
    // 사용자 정보 가져오기
    const res = await axios.get(`/api/v1/users/${route.params.userid}/`, {
      headers: {
        Authorization: `Token ${token}`
      }
    })

    // 찜한 상품 목록 가져오기
    const favoritesRes = await axios.get(`/api/v1/products/favorites/${route.params.userid}/`, {
      headers: {
        Authorization: `Token ${token}`
      }
    })

    user.value = {
      ...res.data,
      followers: res.data.followers || [],
      following: res.data.following || [],
      liked_products: favoritesRes.data || []
    }

    // 최근 게시글 분류
    freePosts.value = res.data.recent_posts.filter(post => post.board_type === '자유게시판')
    questionPosts.value = res.data.recent_posts.filter(post => post.board_type === '질문게시판')

    // 백엔드에서 보내주는 is_following 값을 사용
    isFollowing.value = res.data.is_following

    console.log('사용자 정보:', user.value)
    console.log('팔로우 상태:', isFollowing.value)

  } catch (err) {
    console.error('사용자 정보 로딩 실패:', err)
    if (err instanceof AxiosError) {
      if (err.response?.status === 404) {
        alert('존재하지 않는 사용자입니다.')
        router.push({ name: 'home' })
      } else if (err.response?.status === 401) {
        alert('로그인이 필요한 서비스입니다.')
        router.push({ name: 'login' })
      } else {
        alert('사용자 정보를 불러오는데 실패했습니다.')
      }
    } else {
      alert('네트워크 오류가 발생했습니다.')
    }
  }

  // 투자성향 테스트 결과 가져오기
  try {
    const testRes = await axios.get(`/api/v1/test/result/${route.params.userid}/`, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    user.value.test_result = testRes.data
  } catch (err) {
    if (err.response?.status === 404) {
      user.value.test_result = null
    } else {
      console.error('테스트 결과 로딩 실패:', err)
    }
  }
})

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
}

const handleFollowAction = async () => {
  try {
    const token = accountStore.token
    const targetUserId = user.value.userid  // user_id 대신 userid 사용

    if (isFollowing.value) {
      // 언팔로우
      await axios.delete(`/api/v1/users/${targetUserId}/follow/`, {
        headers: { Authorization: `Token ${token}` }
      })
    } else {
      // 팔로우
      await axios.post(`/api/v1/users/${targetUserId}/follow/`, {}, {
        headers: { Authorization: `Token ${token}` }
      })
    }
    
    // 백엔드 응답의 is_following 값으로 상태 업데이트
    isFollowing.value = !isFollowing.value

    // 팔로워/팔로잉 목록 업데이트를 위해 사용자 정보 다시 불러오기
    const res = await axios.get(`/api/v1/users/${route.params.userid}/`, {
      headers: { Authorization: `Token ${token}` }
    })
    
    user.value = {
      ...res.data,
      followers: res.data.followers || [],
      following: res.data.following || [],
      liked_products: user.value.liked_products  // 기존 찜한 상품 목록 유지
    }

  } catch (error) {
    console.error('팔로우/언팔로우 작업 실패:', error)
    if (error instanceof AxiosError) {
      if (error.response?.status === 401) {
        alert('로그인이 필요한 서비스입니다.')
        router.push({ name: 'login' })
      } else if (error.response?.status === 400) {
        alert('잘못된 요청입니다.')
      } else {
        alert('서버 오류가 발생했습니다.')
      }
    } else {
      alert('네트워크 오류가 발생했습니다.')
    }
  }
}

const goToPost = (type, postId) => {
  const routeName = type === 'free' ? 'freepostdetail' : 'questiondetail'
  router.push({ name: routeName, params: { id: postId } })
}

const goToFollow = () => {
  router.push({ name: 'follow', params: { userid: user.value.userid } })
}

const goToUserPosts = () => {
  router.push({ name: 'userposts', params: { userid: user.value.userid } })
}

const goToProductDetail = (product) => {
  if (product.type === 'deposit') {
    router.push({ name: 'depositdetail', params: { id: product.id } })
  } else if (product.type === 'saving') {
    router.push({ name: 'savingdetail', params: { id: product.id } })
  } else if (product.type === 'stock') {
    router.push({ name: 'stockdetail', params: { stock_code: product.product_code } })
  } else if (product.type === 'etf') {
    router.push({ name: 'etfdetail', params: { etf_code: product.product_code } })
  }
}
</script>

<style scoped>
.mypage-container {
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
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
  background: #145c2b;
  color: white;
  border: none;
}

.follow-button.is-following {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  color: #495057;
}

.follow-button:hover {
  transform: translateY(-2px);
}

.follow-button.is-following:hover {
  background: #dc3545;
  color: white;
  border-color: #dc3545;
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

.content-card:last-child {
  grid-column: 1 / -1;
}

.content-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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

.card-content .posts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #868e96;
}

.empty-state i {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.test-result {
  text-align: center;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.result-header {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.result-type-text {
  font-size: 1.2rem;
  color: #495057;
}

.result-type {
  font-size: 1.5rem;
  font-weight: 700;
  color: #145c2b;
}

.result-score {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 1rem;
}

.like-button {
  padding: 0.3rem 0.8rem;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  background: white;
  color: #495057;
  cursor: pointer;
  transition: all 0.2s;
}

.like-button:hover {
  background: #f8f9fa;
}

.like-button.liked {
  background: #145c2b;
  color: white;
  border-color: #145c2b;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-title {
  cursor: pointer;
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

.product-name {
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.product-info {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #666;
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

.solved-badge {
  background: #145c2b;
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.filter-section {
  margin-bottom: 1.2rem;
  display: flex;
  justify-content: center;
  align-items: flex-end;
}

.filter-buttons.filter-align {
  display: flex;
  gap: 0.4rem;
  justify-content: center;
  align-items: flex-end;
  margin-top: 0.2rem;
}

.filter-button {
  padding: 0.35rem 0.9rem;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  background: white;
  color: #495057;
  cursor: pointer;
  font-size: 0.95rem;
  min-width: 60px;
  height: 2.1rem;
  transition: all 0.2s;
  box-sizing: border-box;
}

.filter-button.active {
  background: #145c2b;
  color: #fff;
  border-color: #145c2b;
}

.filter-button:not(.active):hover {
  background: #e6f4ea;
  color: #145c2b;
  border-color: #b7e2c6;
}

.product-card {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 2rem;
  padding: 1.2rem 1.5rem;
  border-bottom: 1px solid #eee;
  background: #fafbfc;
  border-radius: 10px;
  margin-bottom: 1rem;
}

.product-card:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  font-size: 1rem;
  color: #333;
  flex: 1;
}

.product-header {
  display: flex;
  align-items: center;
  gap: 1.2rem;
}

.product-type-name {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 0.7rem;
}

.product-type {
  font-size: 1rem;
  font-weight: 700;
  color: #145c2b;
  background: #e6f4ea;
  border-radius: 6px;
  padding: 0.2rem 0.7rem;
  margin-right: 0.5rem;
}

.product-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.product-details {
  margin-top: 0.2rem;
  display: flex;
  gap: 2.5rem;
}

.rate-info, .term-info, .price-info, .change-info {
  display: flex;
  gap: 0.5rem;
  font-size: 1rem;
  color: #666;
}

.product-divider {
  display: none;
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
  }

  .profile-stats {
    width: 100%;
    justify-content: space-around;
    margin-top: 1.5rem;
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

  .card-content .posts-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
</style> 