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
            <div class="stat-value">{{ user.following?.length ?? 0 }}</div>
            <div class="stat-label">팔로우</div>
          </div>
          <div class="stat-item" @click="goToFollow">
            <div class="stat-value">{{ user.followers?.length ?? 0 }}</div>
            <div class="stat-label">팔로워</div>
          </div>
          <div class="stat-item" @click="goToMyPosts">
            <div class="stat-value">{{ user.my_posts?.length ?? 0 }}</div>
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
              <div class="result-header">
                <div class="result-type-text">당신은</div>
                <div class="result-type">{{ user.test_result.type }}</div>
              </div>
              <div class="result-score">총점: {{ user.test_result.total_score }}점</div>
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
            <p>첫 게시글을 작성해보세요!</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/users.js'
import { useRouter } from 'vue-router'

const accountStore = useAccountStore()

const router = useRouter()

const user = ref({
  user_id: '',
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
  recent_posts: []
})

const freePosts = ref([])
const questionPosts = ref([])

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

    // API 응답으로 받은 사용자 정보로 업데이트
    user.value = {
      ...res.data,
      followers: res.data.followers || [],
      following: res.data.following || [],
      test_result: res.data.test_result || null  // 테스트 결과도 마이페이지 응답에서 받아옴
    }

    // 최근 게시글 분류
    freePosts.value = res.data.recent_posts?.filter(post => post.board_type === '자유게시판') || []
    questionPosts.value = res.data.recent_posts?.filter(post => post.board_type === '질문게시판') || []

    // localStorage에 최신 사용자 정보 업데이트
    localStorage.setItem('account', JSON.stringify({
      ...JSON.parse(localStorage.getItem('account') || '{}'),
      ...res.data
    }))

    console.log('현재 로그인한 사용자 정보:', user.value)

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

const goToTest = () => {
  router.push({ name: 'investmenttest' })
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
  grid-column: 1 / -1;  /* 마지막 카드(최근 작성글)가 전체 너비를 차지하도록 설정 */
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

.card-actions {
  display: flex;
  gap: 0.5rem;
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

.action-button.primary {
  background: #145c2b;
  color: white;
  border: none;
}

.action-button:hover {
  background: #e9ecef;
}

.action-button.primary:hover {
  background: #0e4a21;
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
}

.empty-state .action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(20, 92, 43, 0.2);
}

.empty-state .action-button i {
  font-size: 1rem;
  margin: 0;
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
    grid-template-columns: 1fr;  /* 모바일에서는 카드들을 세로로 쌓습니다 */
  }

  .content-card:last-child {
    grid-column: auto;  /* 모바일에서는 전체 너비 설정을 해제합니다 */
  }

  .card-content .posts-grid {
    grid-template-columns: 1fr;  /* 모바일에서는 게시판을 세로로 배치합니다 */
    gap: 1.5rem;
  }
}
</style>

