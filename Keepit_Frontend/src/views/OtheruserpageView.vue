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
            <p>아직 투자 성향 테스트를 진행하지 않았습니다.</p>
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
            <p>찜한 상품이 없습니다.</p>
          </div>
        </div>
      </div>

      <!-- 작성 글 카드 -->
      <div class="content-card">
        <div class="card-header">
          <h3>최근 작성글</h3>
          <button class="action-button" @click="goToUserPosts">전체보기</button>
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
            <p>작성한 게시글이 없습니다.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
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
  liked_products: [],
})

const freePosts = ref([])
const questionPosts = ref([])
const isFollowing = ref(false)

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
    const res = await axios.get(`http://127.0.0.1:8000/api/v1/users/${route.params.userid}/`, {
      headers: {
        Authorization: `Token ${token}`
      }
    })

    user.value = {
      ...res.data,
      followers: res.data.followers || [],
      following: res.data.following || [],
    }

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
    }
  ]
})

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
}

const handleFollowAction = async () => {
  try {
    const token = accountStore.token
    const targetUserId = user.value.user_id  // userid가 아닌 user_id를 사용

    if (isFollowing.value) {
      // 언팔로우
      await axios.delete(`http://127.0.0.1:8000/api/v1/users/${targetUserId}/follow/`, {
        headers: { Authorization: `Token ${token}` }
      })
    } else {
      // 팔로우
      await axios.post(`http://127.0.0.1:8000/api/v1/users/${targetUserId}/follow/`, {}, {
        headers: { Authorization: `Token ${token}` }
      })
    }
    
    // 백엔드 응답의 is_following 값으로 상태 업데이트
    isFollowing.value = !isFollowing.value

    // 팔로워/팔로잉 목록 업데이트를 위해 사용자 정보 다시 불러오기
    const res = await axios.get(`http://127.0.0.1:8000/api/v1/users/${route.params.userid}/`, {
      headers: { Authorization: `Token ${token}` }
    })
    
    user.value = {
      ...res.data,
      followers: res.data.followers || [],
      following: res.data.following || [],
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