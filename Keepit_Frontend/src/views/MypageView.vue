<template>
  <div class="mypage-container">
    <!-- 프로필 섹션 -->
    <div class="profile-top">
      <div class="left">
        <div class="profile-image">
          <img src="/images/images_momo/momo_happy.png" alt="프로필 이미지" />
        </div>
        <div class="user-info">
          <p><strong>{{ user.nickname }}</strong> ({{ user.userid }})</p>
        </div>
      </div>

      <div class="right">
        <div class="stats-box">
          <div class="stat" @click="goToFollow">
            <span>팔로우</span>
            <strong>{{ user.following?.length ?? 0 }}</strong>
          </div>
          <div class="stat" @click="goToFollow">
            <span>팔로워</span>
            <strong>{{ user.followers?.length ?? 0 }}</strong>
          </div>
          <div class="stat" @click="goToMyPosts" style="cursor: pointer;">
            <span>내가 쓴 글</span>
            <strong>{{ user.my_posts?.length ?? 0 }}</strong>
          </div>
        </div>
        <div class="buttons">
          <button @click="goToEdit">내 정보 수정</button>
        </div>
      </div>
    </div>

    <!-- 성향 테스트 결과 -->
    <div class="section">
      <div class="section-header">
        <h4>성향 테스트 결과</h4>
        <div class="test-actions">
          <button v-if="user.test_result" class="view-result" @click="goToTestResult">
            결과 자세히 보기
          </button>
          <button class="take-test" @click="goToTest">
            {{ user.test_result ? '테스트 다시하기' : '테스트 하러가기' }}
          </button>
        </div>
      </div>
      
      <div v-if="user.test_result" class="test-result-preview">
        <div class="result-type">
          <strong>{{ user.test_result.type }}</strong>
          <span class="score">{{ user.test_result.total_score }}점</span>
        </div>
        <p class="result-description">{{ user.test_result.description }}</p>
      </div>
      <div v-else class="no-result">
        아직 성향 테스트를 완료하지 않았습니다.
      </div>
    </div>

    <!-- 찜한 상품 -->
    <div class="section">
      <h4>찜한 상품</h4>
      <template v-if="user.liked_products?.length">
        <ul>
          <li v-for="product in user.liked_products" :key="product.id">
            {{ product.name }} - {{ product.bank }} /
            {{ product.interest_rate }} ~ {{ product.special_rate }}% /
            {{ product.term }}개월
          </li>
        </ul>
      </template>
      <template v-else>
        <p>찜한 상품이 없습니다.</p>
      </template>
    </div>

    <!-- 내가 쓴 글 -->
    <div class="section">
      <div class="section-header">
        <h4>내가 쓴 글</h4>
        <button class="view-all" @click="goToMyPosts">전체보기</button>
      </div>
      
      <!-- 자유 게시판 -->
      <div class="posts-section" v-if="freePosts.length">
        <h5>자유 게시판</h5>
        <ul class="posts-list">
          <li v-for="post in freePosts.slice(0, 3)" :key="post.id" @click="goToPost('free', post.id)">
            <div class="post-title">{{ post.title }}</div>
            <div class="post-info">
              <span class="post-date">{{ formatDate(post.created_at) }}</span>
              <span class="post-likes">공감 {{ post.likes }}</span>
            </div>
          </li>
        </ul>
      </div>

      <!-- 질문 게시판 -->
      <div class="posts-section" v-if="questionPosts.length">
        <h5>질문 게시판</h5>
        <ul class="posts-list">
          <li v-for="post in questionPosts.slice(0, 3)" :key="post.id" @click="goToPost('question', post.id)">
            <div class="post-title">
              {{ post.title }}
              <span class="solved-badge" v-if="post.is_solved">해결됨</span>
            </div>
            <div class="post-info">
              <span class="post-date">{{ formatDate(post.created_at) }}</span>
              <span class="post-likes">공감 {{ post.likes }}</span>
            </div>
          </li>
        </ul>
      </div>

      <div v-if="!freePosts.length && !questionPosts.length" class="no-posts">
        작성한 글이 없습니다.
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

const token = accountStore.token  // token은 ref
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
  // my_posts: [],
  // test_result: null,
  // liked_products: [],
})

const freePosts = ref([])
const questionPosts = ref([])

onMounted(async () => {
  const raw = localStorage.getItem('account')
  const parsed = raw ? JSON.parse(raw) : null
  const localToken = parsed?.token
  const localUserId = parsed?.user_id

  if (!localToken || !localUserId) {
    alert('⚠️ 로그인 정보가 없습니다. 다시 로그인해주세요.')
    router.push({ name: 'login' })
    return
  }

  // localStorage의 실제 사용자 정보 사용
  user.value = {
    userid: parsed.userid || 'keepit22',  // localStorage에서 확인된 아이디
    user_id: localUserId,  // 2
    nickname: parsed.nickname || '키핏이',
    followers: [],
    following: [],
    my_posts: [],
    test_result: null,
    liked_products: []
  }

  console.log('현재 로그인한 사용자 정보:', user.value)
  console.log('localStorage account 정보:', parsed)

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

  // 이제 백엔드 연결을 시도해보겠습니다.
  try {
    const [userRes, postsRes] = await Promise.all([
      axios.get('http://localhost:8000/api/v1/users/mypage/', {
        headers: {
          Authorization: `Token ${localToken}`
        }
      }),
      axios.get('http://localhost:8000/api/v1/community/my-posts/', {
        headers: {
          Authorization: `Token ${localToken}`
        }
      })
    ])

    if (userRes.data) {
      user.value = { ...user.value, ...userRes.data }
    }

    if (Array.isArray(postsRes.data)) {
      freePosts.value = postsRes.data.filter(post => post.type === 'free' || post.board_type === 'free')
      questionPosts.value = postsRes.data.filter(post => post.type === 'question' || post.board_type === 'question')
    }
  } catch (err) {
    console.error('❌ 마이페이지 로딩 실패:', err)
    console.log('에러 상세:', err.response || err)
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
  router.push({ name: 'followlist', params: { userid: accountStore.userId } })
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
  max-width: 900px;
  margin: auto;
  padding: 2rem;
  font-family: 'Pretendard', sans-serif;
}

.profile-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background-color: #f9f9f9;
  padding: 1.5rem;
  border-radius: 10px;
}

.left {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.8rem;
}

.profile-image {
  width: 300px;
  height: 300px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-info p {
  margin: 0.2rem 0;
  color: #333;
}

.right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.stats-box {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.stat {
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 0.8rem 1.2rem;
  text-align: center;
  min-width: 100px;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.05);
}

.stat span {
  display: block;
  font-weight: bold;
  color: #444;
}

.stat strong {
  display: block;
  font-size: 1.1rem;
  margin-top: 0.4rem;
}

.buttons button {
  border: 2px solid #145c2b;
  color: #145c2b;
  background-color: white;
  padding: 0.5rem 1.3rem;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}

.buttons button:hover {
  background-color: #145c2b;
  color: white;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.view-all {
  background: none;
  border: none;
  color: #145c2b;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.view-all:hover {
  background: rgba(20, 92, 43, 0.1);
}

.posts-section {
  margin-bottom: 2rem;
}

.posts-section h5 {
  font-size: 1.1rem;
  color: #444;
  margin-bottom: 1rem;
}

.posts-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.posts-list li {
  background: white;
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.posts-list li:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.post-title {
  font-weight: 500;
  color: #333;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.post-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #666;
}

.solved-badge {
  background: #145c2b;
  color: white;
  font-size: 0.8rem;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
}

.no-posts {
  text-align: center;
  padding: 2rem;
  color: #666;
  background: #f9f9f9;
  border-radius: 8px;
}

.test-actions {
  display: flex;
  gap: 0.8rem;
}

.view-result, .take-test {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.view-result {
  background-color: white;
  color: #145c2b;
  border: 1px solid #145c2b;
}

.take-test {
  background-color: #145c2b;
  color: white;
  border: none;
}

.view-result:hover {
  background-color: #f0f8f3;
}

.take-test:hover {
  background-color: #0d4420;
}

.test-result-preview {
  background: white;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 1.2rem;
}

.result-type {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.8rem;
}

.result-type strong {
  color: #145c2b;
  font-size: 1.2rem;
}

.score {
  color: #666;
  font-size: 0.9rem;
}

.result-description {
  color: #444;
  line-height: 1.5;
}

.no-result {
  text-align: center;
  padding: 2rem;
  color: #666;
  background: #f9f9f9;
  border-radius: 8px;
}
</style>
