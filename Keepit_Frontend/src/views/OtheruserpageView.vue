<template>
  <div class="mypage-container">
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
          <div class="stat"><span>팔로우</span><strong>{{ user.following.length }}</strong></div>
          <div class="stat"><span>팔로워</span><strong>{{ user.followers.length }}</strong></div>
          <div class="stat"><span>찜한 상품</span><strong>{{ likedProducts.length }}</strong></div>
        </div>
        <div class="buttons">
          <button @click="toggleFollow">{{ isFollowing ? '언팔로우' : '팔로우' }}</button>
        </div>
      </div>
    </div>

    <div class="section">
      <h4>성향 테스트 결과</h4>
      <p><strong>{{ user.test_result?.type }}</strong></p>
      <p>{{ user.test_result?.description }}</p>
    </div>

    <div class="section" v-if="likedProducts.length">
      <h4>찜한 상품 목록</h4>
      <ul>
        <li v-for="product in likedProducts" :key="product.id">
          {{ product.name }} ({{ product.bank }}) - {{ product.interest_rate }}% ~ {{ product.special_rate }}%
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/users.js'

const accountStore = useAccountStore()
const { token, userId } = accountStore
const route = useRoute()

const user = ref({
  nickname: '',
  userid: '',
  followers: [],
  following: [],
  test_result: {},
})
const likedProducts = ref([])
const isFollowing = ref(false)

onMounted(async () => {
  const targetUserId = route.params.userId
  try {
    const res = await axios.get(`/api/v1/users/${targetUserId}/`, {
      headers: { Authorization: `Token ${token}` }
    })
    user.value = res.data.data
    likedProducts.value = res.data.data.liked_products || []
    isFollowing.value = res.data.data.is_following  // 백에서 알려주는 경우
  } catch (err) {
    console.error('❌ 사용자 정보 조회 실패', err)
  }
})

const toggleFollow = async () => {
  const targetUserId = route.params.userId
  try {
    if (isFollowing.value) {
      await axios.delete(`/api/v1/users/${targetUserId}/follow/`, {
        headers: { Authorization: `Token ${token}` },
      })
      isFollowing.value = false
    } else {
      await axios.post(`/api/v1/users/${targetUserId}/follow/`, {}, {
        headers: { Authorization: `Token ${token}` },
      })
      isFollowing.value = true
    }
  } catch (err) {
    console.error('❌ 팔로우 토글 실패', err)
  }
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
</style>
