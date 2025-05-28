<template>
  <div class="follow-page">
    <h2>팔로우 / 팔로워 목록</h2>
    
    <div class="follow-sections">
      <div class="follow-section">
        <h3>팔로우 <span class="count">({{ following.length }})</span></h3>
        <ul>
          <li v-if="following.length === 0">팔로잉한 사용자가 없습니다.</li>
          <li v-for="user in following" :key="user.user_id" class="user-item">
            <a @click="goToUserPage(user.userid)">
              {{ user.nickname }} ({{ user.userid }})
            </a>
          </li>
        </ul>
      </div>

      <div class="follow-section">
        <h3>팔로워 <span class="count">({{ followers.length }})</span></h3>
        <ul>
          <li v-if="followers.length === 0">팔로워가 없습니다.</li>
          <li v-for="user in followers" :key="user.user_id" class="user-item">
            <a @click="goToUserPage(user.userid)">
              {{ user.nickname }} ({{ user.userid }})
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/users.js'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()
const { token } = accountStore

const followers = ref([])
const following = ref([])

const goToUserPage = (userid) => {
  router.push({ name: 'userpage', params: { userid } })
}

onMounted(async () => {
  const userid = route.params.userid
  const url = `http://127.0.0.1:8000/api/v1/users/follow-info/${userid}/`

  try {
    const res = await axios.get(url, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    followers.value = res.data.data.followers
    following.value = res.data.data.following
  } catch (err) {
    console.error('❌ 팔로우 정보 불러오기 실패:', err)
    alert('팔로우 정보를 불러오는 데 실패했습니다.')
  }
})
</script>

<style scoped>
.follow-page {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  font-family: 'Pretendard', sans-serif;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #145c2b;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.5rem;
  font-weight: bold;
}

.follow-sections {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.follow-section {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
}

h3 {
  color: #145c2b;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #145c2b;
  font-size: 1.2rem;
}

.count {
  color: #666;
  font-size: 0.9rem;
  font-weight: normal;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 400px;
  overflow-y: auto;
}

.user-item {
  padding: 0.8rem;
  background-color: white;
  margin-bottom: 0.5rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.user-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-item a {
  color: #145c2b;
  text-decoration: none;
  cursor: pointer;
  display: block;
}

.user-item a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .follow-sections {
    grid-template-columns: 1fr;
  }
  
  .follow-page {
    margin: 1rem;
    padding: 1rem;
  }
}
</style>
