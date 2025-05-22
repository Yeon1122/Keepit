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
          <div class="stat" @click="goToFollow"><span>팔로우</span><strong>{{ user.following.length }}</strong></div>
          <div class="stat" @click="goToFollow"><span>팔로워</span><strong>{{ user.followers.length }}</strong></div>
          <div class="stat"><span>내가 쓴 글</span><strong>{{ user.my_posts.length }}</strong></div>
        </div>
        <div class="buttons">
          <button @click="goToEdit">내 정보 수정</button>
        </div>
      </div>
    </div>

    <!-- 성향 테스트 결과 -->
    <div v-if="user.test_result" class="section">
      <h4>성향 테스트 결과</h4>
      <p><strong>{{ user.test_result.type }}</strong></p>
      <p>{{ user.test_result.description }}</p>
    </div>

    <!-- 찜한 상품 -->
    <div v-if="user.liked_products?.length" class="section">
      <h4>찜한 상품</h4>
      <ul>
        <li v-for="product in user.liked_products" :key="product.id">
          {{ product.name }} - {{ product.bank }} / {{ product.interest_rate }} ~ {{ product.special_rate }}% / {{ product.term }}개월
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/users.js'
import { useRouter } from 'vue-router'

const accountStore = useAccountStore()
const { token } = accountStore
const router = useRouter()

const user = ref({
  nickname: '',
  userid: '',
  followers: [],
  following: [],
  my_posts: [],
  test_result: null,
  liked_products: []
})

onMounted(async () => {
  try {
    const res = await axios.get('/api/v1/users/mypage/', {
      headers: {
        Authorization: `Token ${token}`,
      }
    })
    user.value = res.data.data
  } catch (err) {
    console.error('❌ 마이페이지 로딩 실패:', err)
    alert('마이페이지 정보를 불러오는 데 실패했습니다.')
  }
})

const goToEdit = () => {
  router.push({ name: 'useredit' })
}

const goToFollow = () => {
  router.push({ name: 'followlist' })
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
  flex-direction: column; /* ⬅ 변경: 이미지 아래에 텍스트 */
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
  box-shadow: 0 0 3px rgba(0,0,0,0.05);
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
</style>