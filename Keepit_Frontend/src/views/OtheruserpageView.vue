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
          <div class="stat">
            <span>내가 쓴 글</span>
            <strong>{{ user.my_posts?.length ?? 0 }}</strong>
          </div>
        </div>
        <div class="buttons">
          <button 
            v-if="isAuthenticated && !isOwnProfile" 
            @click="toggleFollow" 
            :class="{ 'followed': isFollowing, 'unfollowed': !isFollowing }"
          >
            {{ isFollowing ? '언팔로우' : '팔로우' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 성향 테스트 결과 -->
    <div class="section">
      <h4>성향 테스트 결과</h4>
      <template v-if="user.test_result">
        <p><strong>{{ user.test_result.type }}</strong></p>
        <p>{{ user.test_result.description }}</p>
      </template>
      <template v-else>
        <p>성향 테스트 결과가 없습니다.</p>
      </template>
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

    <!-- 작성한 글 -->
    <div class="section">
      <h4>작성한 글</h4>
      
      <!-- 자유 게시판 -->
      <div class="posts-section" v-if="freePosts.length">
        <h5>자유 게시판</h5>
        <ul class="posts-list">
          <li v-for="post in freePosts.slice(0, 3)" :key="post.id" @click="goToPost('free', post.id)">
            <div class="post-title">{{ post.title }}</div>
            <div class="post-info">
              <span class="post-date">{{ formatDate(post.created_at) }}</span>
              <LikeButton
                :initial-is-liked="post.is_liked"
                :initial-count="post.likes"
                :show-count="true"
              />
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
              <LikeButton
                :initial-is-liked="post.is_liked"
                :initial-count="post.likes"
                :show-count="true"
              />
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
import { ref, onMounted, watchEffect, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/users.js'
import LikeButton from '@/components/LikeButton.vue'

const accountStore = useAccountStore()
const { token, userId } = accountStore
const route = useRoute()
const router = useRouter()

const isAuthenticated = computed(() => accountStore.isAuthenticated)
const currentUserId = computed(() => accountStore.user_id)

const isOwnProfile = computed(() => {
    return user.value && currentUserId.value === user.value.user_id
})

// watchEffect(() => {
//   const targetUserid = route.params.userid
//   const myUserid = accountStore.user_id

//   if (myUserid && String(targetUserid) === String(myUserid)) {
//     router.push({ name: 'mypage' })
//   }
// })

const user = ref({
  nickname: '',
  userid: '',
  user_id: '',
  followers: [],
  following: [],
  test_result: {},
})
const likedProducts = ref([])
const isFollowing = ref(false)
const freePosts = ref([])
const questionPosts = ref([])

onMounted(async () => {
  const targetUserid = route.params.userid

  if (String(targetUserid) === accountStore.userId) {
    router.push({ name: 'mypage' })
    return
  }

  try {
    const res = await axios.get(`http://localhost:8000/api/v1/users/${targetUserid}/`, {
      headers: { Authorization: `Token ${token}` }
    })

    user.value = res.data
    likedProducts.value = res.data.liked_products || []
    isFollowing.value = res.data.is_following

    if (Array.isArray(res.data.posts)) {
      freePosts.value = res.data.posts.filter(post => post.type === 'free' || post.board_type === 'free')
      questionPosts.value = res.data.posts.filter(post => post.type === 'question' || post.board_type === 'question')
    }
  } catch (err) {
    console.error('❌ 사용자 정보 조회 실패', err)
    alert('존재하지 않는 유저입니다.')
    window.history.back()
  }
})

const toggleFollow = async () => {
  const targetUserPk = user.value.user_id

  try {
    let res
    if (isFollowing.value) {
      res = await axios.delete(`http://localhost:8000/api/v1/users/${targetUserPk}/follow/`, {
        headers: { Authorization: `Token ${token}` },
      })
    } else {
      res = await axios.post(`http://localhost:8000/api/v1/users/${targetUserPk}/follow/`, {}, {
        headers: { Authorization: `Token ${token}` },
      })
    }

    // ✅ 응답 기반으로 바로 상태 업데이트
    isFollowing.value = res.data.data.is_following
    user.value.followers = res.data.data.followers
    user.value.following = res.data.data.following

  } catch (err) {
    console.error('❌ 팔로우 토글 실패', err)
  }
}

const goToFollow = () => {
  const targetUserid = route.params.userid
  router.push({ name: 'followlist', params: { userid: targetUserid } })
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
}

const goToPost = (type, postId) => {
  const routeName = type === 'free' ? 'freepostdetail' : 'questiondetail'
  router.push({ name: routeName, params: { id: postId } })
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
  background-color: #f9f9f9;
  padding: 1.5rem;
  border-radius: 10px;
}

.left {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
}

.profile-image {
  width: 150px;
  height: 150px;
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
  text-align: center;
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

.section {
  margin-top: 2rem;
  border-top: 1px solid #ccc;
  padding-top: 1rem;
}

.buttons button.unfollowed {
  background-color: #145c2b;
  color: white;
  border: 2px solid #145c2b;
}

.buttons button.followed {
  background-color: white;
  color: #145c2b;
  border: 2px solid #145c2b;
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

.post-meta,
.comment-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}
</style>