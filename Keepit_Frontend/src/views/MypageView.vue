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
                <span class="result-type">{{ user.test_result.type }}</span>
                <span class="result-score">{{ user.test_result.total_score }}점</span>
              </div>
              <p class="result-description">{{ user.test_result.description }}</p>
            </div>
          </template>
          <div v-else class="empty-state">
            <i class="fas fa-chart-line"></i>
            <p>투자 성향 테스트를 진행해보세요!</p>
          </div>
        </div>
      </div>

      <!-- 찜한 상품 카드 -->
      <div class="content-card">
        <div class="card-header">
          <h3>찜한 상품</h3>
        </div>
        <div class="card-content">
          <template v-if="user.liked_products?.length">
            <ul class="product-list">
              <li v-for="product in user.liked_products" :key="product.id" class="product-item">
                <div class="product-name">{{ product.name }}</div>
                <div class="product-info">
                  <span class="bank">{{ product.bank }}</span>
                  <span class="rate">{{ product.interest_rate }}% ~ {{ product.special_rate }}%</span>
                  <span class="term">{{ product.term }}개월</span>
                </div>
              </li>
            </ul>
          </template>
          <div v-else class="empty-state">
            <i class="fas fa-heart"></i>
            <p>관심있는 상품을 찜해보세요!</p>
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
                      <span class="post-likes">
                        <i class="fas fa-heart"></i> {{ post.likes }}
                      </span>
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
                      <span class="post-likes">
                        <i class="fas fa-heart"></i> {{ post.likes }}
                      </span>
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
    const res = await axios.get('http://127.0.0.1:8000/api/v1/users/mypage/', {
      headers: {
        Authorization: `Token ${token}`
      }
    })

    // API 응답으로 받은 사용자 정보로 업데이트
    user.value = {
      ...res.data,
      followers: res.data.followers || [],
      following: res.data.following || [],
    }

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
    }
  }

  // 더미 게시글 데이터는 유지
  freePosts.value = [
    {
      id: 1,
      title: '적금 드디어 만기!',
      content: '2년동안 열심히 모았네요. 다들 화이팅하세요!',
      created_at: '2024-03-15T10:00:00',
      likes: 15,
      comments: [1, 2, 3]
    },
    {
      id: 2,
      title: '재테크 시작하려고 합니다',
      content: '첫 직장인이라 재테크 공부중입니다.',
      created_at: '2024-03-14T15:30:00',
      likes: 8,
      comments: [1, 2]
    }
  ]

  questionPosts.value = [
    {
      id: 1,
      title: '적금 중도해지 어떻게 하나요?',
      content: '급하게 돈이 필요한데 중도해지 절차가 궁금합니다.',
      created_at: '2024-03-13T09:00:00',
      likes: 5,
      comments: [1, 2, 3, 4],
      is_solved: true
    },
    {
      id: 2,
      title: '주택청약 가입 조건이 어떻게 되나요?',
      content: '내년에 청약을 하려고 하는데 조건이 궁금합니다.',
      created_at: '2024-03-12T14:20:00',
      likes: 12,
      comments: [1],
      is_solved: false
    }
  ]
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
  router.push({ name: 'testresult' })
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
  color: #868e96;
}

.empty-state i {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.test-result {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.result-type {
  font-weight: 700;
  color: #145c2b;
}

.result-score {
  color: #495057;
  font-size: 0.9rem;
}

.result-description {
  color: #495057;
  line-height: 1.6;
  margin: 0;
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

.post-title {
  font-weight: 500;
  color: #333;
  margin-bottom: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.solved-badge {
  background: #145c2b;
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  color: #868e96;
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

