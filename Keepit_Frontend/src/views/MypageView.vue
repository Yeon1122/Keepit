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
            <button @click="goToEdit" class="edit-button">
              <i class="fas fa-edit"></i> 프로필 수정
            </button>
          </div>
        </div>
        <div class="profile-stats">
          <div class="stat-item" @click="goToFollow">
            <div class="stat-value">{{ user.following && user.following.length ? user.following.length : 0 }}</div>
            <div class="stat-label">팔로우</div>
          </div>
          <div class="stat-item" @click="goToFollow">
            <div class="stat-value">{{ user.followers && user.followers.length ? user.followers.length : 0 }}</div>
            <div class="stat-label">팔로워</div>
          </div>
          <div class="stat-item" @click="goToMyPosts">
            <div class="stat-value">{{ user.posts_summary && user.posts_summary.total_posts ?
              user.posts_summary.total_posts : 0 }}</div>
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
          <div class="card-actions">
            <button v-if="user.test_result" class="action-button" @click="goToTestResult">
              결과 상세
            </button>
            <button class="action-button primary" @click="goToTest">
              {{ user.test_result ? '다시하기' : '테스트하기' }}
            </button>
          </div>
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
                  <div v-for="(isRecommended, type) in user.test_result.recommendations" :key="type"
                    class="recommendation-chip" :class="{ 'recommended': isRecommended }">
                    {{ getProductTypeDisplay(type) }}
                  </div>
                </div>
              </div>
            </div>
          </template>
          <div v-else class="empty-state">
            <i class="fas fa-chart-line"></i>
            <p>아직 투자 성향 테스트를 하지 않으셨네요!</p>
            <p class="sub-text">나의 투자 성향을 알아보고 맞춤 상품을 추천받아보세요.</p>
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
          <template v-if="limitedFilteredProducts.length">
            <div class="product-card" v-for="product in limitedFilteredProducts" :key="product.id">
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
                <button v-if="filteredProducts.length > 1" class="view-more-button" @click="goToFavorites">
                  더보기
                  <i class="fas fa-chevron-right"></i>
                </button>
              </div>
              <div class="product-divider"></div>
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

      <!-- 작성 글 카드 -->
      <div class="content-card">
        <div class="card-header">
          <h3>최근 작성글</h3>
          <button class="action-button" @click="goToMyPosts">전체보기</button>
        </div>
        <div class="card-content">
          <div v-if="freePosts.length || questionPosts.length" class="posts-grid">
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
                        <i class="fas fa-comment"></i> {{ Array.isArray(post.comments) ? post.comments.length : 0 }}
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
                        <i class="fas fa-comment"></i> {{ Array.isArray(post.comments) ? post.comments.length : 0 }}
                      </span>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>

          <!-- 게시글이 없을 때 -->
          <div v-else class="empty-state">
            <i class="fas fa-pen"></i>
            <p>첫 게시글을 작성해보세요!</p>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/users.js'
import { useRouter } from 'vue-router'

const accountStore = useAccountStore()
const router = useRouter()

const user = ref({
  userid: '',
  nickname: '',
  name: '',
  email: '',
  birth_year: '',
  birth_month: '',
  birth_day: '',
  region_city: '',
  region_district: '',
  followers: [],
  following: [],
  test_result: null,
  posts_summary: {
    total_posts: 0,
    free_posts: 0,
    question_posts: 0
  },
  recent_posts: [],
  liked_products: [],
  my_posts: []
})

const freePosts = ref([])
const questionPosts = ref([])

// 필터 상태 추가
const selectedFilter = ref('all')

// 필터링된 상품 목록을 계산하는 computed 속성 수정
const filteredProducts = computed(() => {
  const products = user.value.liked_products || []
  if (selectedFilter.value === 'all') {
    return products
  }
  return products.filter(product => product.type === selectedFilter.value)
})

// 필터링된 상품 목록에서 최대 1개만 보여주는 computed 속성
const limitedFilteredProducts = computed(() => {
  return filteredProducts.value.slice(0, 1)
})

// 빈 상태 메시지를 동적으로 생성하는 computed 속성
const getEmptyStateMessage = computed(() => {
  if (selectedFilter.value === 'all') {
    return '아직 찜한 상품이 없습니다.'
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

onMounted(async () => {
  const token = accountStore.token
  const userId = accountStore.userId

  if (!token || !userId) {
    alert('⚠️ 로그인 정보가 없습니다. 다시 로그인해주세요.')
    router.push({ name: 'login' })
    return
  }

  try {
    // 마이페이지 정보 가져오기
    const res = await axios.get('/api/v1/users/mypage/', {
      headers: {
        Authorization: `Token ${token}`
      }
    })

    // 찜한 상품 목록 가져오기
    const favoritesRes = await axios.get('/api/v1/products/favorites/', {
      headers: {
        Authorization: `Token ${token}`
      }
    })

    // API 응답으로 받은 사용자 정보로 업데이트
    user.value = {
      ...res.data,
      followers: res.data.followers || [],
      following: res.data.following || [],
      test_result: res.data.test_result || null,
      liked_products: favoritesRes.data || [],
      posts_summary: res.data.posts_summary || { total_posts: 0, free_posts: 0, question_posts: 0 }
    }

    // 최근 게시글 분류
    if (Array.isArray(res.data.recent_posts)) {
      freePosts.value = res.data.recent_posts.filter(post => post && post.board_type === '자유게시판') || []
      questionPosts.value = res.data.recent_posts.filter(post => post && post.board_type === '질문게시판') || []
    } else {
      freePosts.value = []
      questionPosts.value = []
    }

    // localStorage에 최신 사용자 정보 업데이트
    localStorage.setItem('account', JSON.stringify({
      ...JSON.parse(localStorage.getItem('account') || '{}'),
      ...res.data
    }))

    console.log('현재 로그인한 사용자 정보:', user.value)
    console.log('찜한 상품 목록:', favoritesRes.data)  // 디버깅용 로그

  } catch (err) {
    console.error('사용자 정보 로딩 실패:', err)
    if (err.response?.status === 401) {
      alert('로그인이 만료되었습니다. 다시 로그인해주세요.')
      accountStore.logOut()
      router.push({ name: 'login' })
    } else {
      alert('사용자 정보를 불러오는데 실패했습니다.')
    }
  }

  // 투자성향 테스트 결과 가져오기
  try {
    const testRes = await axios.get('/api/v1/test/result/', {
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

const goToPost = (type, postId) => {
  const routeName = type === 'free' ? 'freepostdetail' : 'questiondetail'
  router.push({ name: routeName, params: { id: postId } })
}

const goToEdit = () => {
  router.push({ name: 'useredit' })
}

const goToFollow = () => {
  router.push({ name: 'follow', params: { userid: accountStore.userId } })
}

const goToMyPosts = () => {
  router.push({ name: 'myposts' })
}

const goToTest = async () => {
  console.log('🎯 마이페이지 - 투자 스타일 테스트 버튼 클릭됨')

  try {
    // 기존 검사 결과 확인
    const response = await axios.get('/api/v1/test/result/')
    console.log('📊 검사 결과 응답:', response.data)

    if (response.data && response.data.type) {
      console.log('✅ 기존 검사 결과 있음:', response.data.type)
      // 기존 검사 결과가 있는 경우
      const userChoice = confirm('이미 투자 성향 검사를 받으셨습니다.\n\n다시 검사를 받으시겠습니까?\n\n확인: 새로 검사받기\n취소: 기존 결과 보기')
      console.log('👤 사용자 선택:', userChoice ? '새로 검사받기' : '기존 결과 보기')

      if (userChoice) {
        // 새로 검사받기
        router.push({ name: 'investmenttest' })
      } else {
        // 기존 결과 보기
        router.push({ name: 'testresult' })
      }
    } else {
      console.log('❌ 검사 결과 없음, 테스트로 이동')
      // 검사 결과가 없는 경우 바로 테스트로 이동
      router.push({ name: 'investmenttest' })
    }
  } catch (error) {
    console.error('❌ 검사 결과 확인 중 오류:', error)
    if (error.response?.status === 404) {
      console.log('📝 404 오류 - 검사 결과 없음, 테스트로 이동')
      // 검사 결과가 없는 경우 바로 테스트로 이동
      router.push({ name: 'investmenttest' })
    } else {
      console.error('🚨 기타 오류, 테스트로 이동')
      // 오류가 발생해도 테스트로 이동
      router.push({ name: 'investmenttest' })
    }
  }
}

const goToTestResult = () => {
  if (!user.value.test_result) {
    alert('테스트 결과가 없습니다. 테스트를 먼저 진행해주세요.')
    router.push({ name: 'investmenttest' })
    return
  }
  router.push({ name: 'testresult' })
}

const goToSavings = () => {
  router.push({ name: 'savings' })
}

const goToFavorites = () => {
  router.push({ name: 'myfavorites' })
}

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

// 상품명 가져오는 함수 수정
const getProductName = (product) => {
  return product.name
}

// 가격 포맷팅 함수 추가
const formatPrice = (price) => {
  if (!price) return '0'
  return price.toLocaleString()
}

// 가격 변동 포맷팅 함수 추가
const formatPriceChange = (change) => {
  if (!change) return '0'
  return Math.abs(change).toLocaleString()
}

// 가격 변동에 따른 클래스 반환 함수 추가
const getPriceChangeClass = (change) => {
  if (!change) return ''
  return change > 0 ? 'price-up' : 'price-down'
}

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

.edit-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  color: #495057;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.edit-button:hover {
  background: #e9ecef;
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
  /* 마지막 카드(최근 작성글)가 전체 너비를 차지하도록 설정 */
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

.card-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.action-button {
  padding: 0.5rem 1rem;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  background: white;
  color: #145c2b;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.action-button:hover {
  background: #f8f9fa;
}

.action-button.primary {
  background: #145c2b;
  color: white;
  border-color: #145c2b;
}

.action-button.primary:hover {
  background: #0d4420;
}

.card-content {
  flex: 1;
  /* card-header를 제외한 나머지 공간을 차지하도록 설정 */
  display: flex;
  align-items: center;
  /* 수직 중앙 정렬 */
  justify-content: center;
  /* 수평 중앙 정렬 */
  padding: 2rem;
}

.card-content .posts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  width: 100%;
  /* 그리드가 전체 너비를 사용하도록 설정 */
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

.empty-state .action-button {
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  background: #145c2b;
  color: white;
  border-color: #145c2b;
}

.empty-state .action-button i {
  font-size: 1rem;
  margin: 0;
  color: rgba(255, 255, 255, 0.85);
  transition: color 0.3s ease;
}

.empty-state .action-button:hover {
  background: #0d4420;
}

.empty-state .action-button:hover i {
  color: rgba(255, 255, 255, 1);
}

/* 투자 성향 분석 카드의 empty-state에만 적용되는 스타일 */
.content-card:first-child .card-content {
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.content-card:first-child .empty-state {
  padding: 0;
  width: 100%;
}

.content-card:first-child .empty-state i {
  margin-bottom: 1.5rem;
}

.content-card:first-child .empty-state p {
  margin: 0.8rem 0;
}

.test-result {
  width: 100%;
  text-align: center;
  padding: 2rem;
  background: hwb(0 100% 0%);
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
  background-color: #f1fcf4;
  border-color: #145c2b;
  color: #145c2b;
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
  font-size: 0.85rem;
  color: #666;
}

.post-title {
  font-size: 1rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.product-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.product-item {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s ease;
  cursor: pointer;
}

.product-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.product-info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.product-type {
  background-color: #145c2b;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.bank-name {
  color: #666;
  font-size: 0.9rem;
}

.product-name {
  font-size: 1.1rem;
  font-weight: bold;
  color: #145c2b;
  margin-bottom: 0.5rem;
}

.product-details {
  display: grid;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.rate-info,
.term-info,
.price-info,
.volume-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  color: #666;
  font-size: 0.9rem;
}

.value {
  font-weight: 600;
  color: #145c2b;
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
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #eee;
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
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
  display: flex;
  justify-content: center;
  padding: 1rem 0;
}

.view-more-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.6rem;
  margin-top: 1rem;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  background: white;
  color: #495057;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
  width: 100%;
}

.view-more-button:hover {
  background: #f8f9fa;
  color: #145c2b;
  border-color: #145c2b;
}

.view-more-button i {
  font-size: 0.8rem;
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
    /* 모바일에서는 카드들을 세로로 쌓습니다 */
  }

  .content-card:last-child {
    grid-column: auto;
    /* 모바일에서는 전체 너비 설정을 해제합니다 */
  }

  .card-content .posts-grid {
    grid-template-columns: 1fr;
    /* 모바일에서는 게시판을 세로로 배치합니다 */
    gap: 1.5rem;
  }

  .card-header {
    flex-direction: row;
    /* 모바일에서도 가로 배치 유지 */
    align-items: center;
    padding: 1rem;
  }

  .filter-section {
    padding: 1rem;
  }

  .filter-buttons {
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }

  .filter-button {
    white-space: nowrap;
  }

  .card-actions {
    gap: 0.25rem;
    /* 모바일에서는 버튼 간격 줄임 */
  }

  .action-button {
    padding: 0.4rem 0.8rem;
    /* 모바일에서는 버튼 크기 줄임 */
    font-size: 0.85rem;
  }
}

.product-card {
  width: 100%;
  padding: 0.8rem 1.5rem;
}

.product-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.8rem;
  /* 하단 마진 줄임 */
}

.product-type {
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 500;
  color: white;
  background-color: #145c2b;
}

.product-title {
  font-size: 1.1rem;
  color: #333;
  font-weight: 500;
}

.product-details {
  display: grid;
  gap: 0.4rem;
  /* 상세 정보 간격 줄임 */
}

.rate-info,
.term-info,
.price-info,
.change-info {
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

.price-up {
  color: #d63031;
  display: flex;
  align-items: center;
  gap: 0.2rem;
}

.price-down {
  color: #0984e3;
  display: flex;
  align-items: center;
  gap: 0.2rem;
}

.price-up i,
.price-down i {
  font-size: 1.2rem;
}

.product-divider {
  margin: 0.8rem -1.5rem;
  /* 구분선 위아래 마진 줄임 */
  height: 1px;
  background-color: #eee;
}

/* 마지막 상품의 구분선 제거 */
.product-card:last-child .product-divider {
  display: none;
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
</style>
