<template>
  <div class="follow-page">
    <h2>팔로우 / 팔로워 목록</h2>
    <div class="follow-section">
      <h3>팔로잉</h3>
      <ul>
        <li v-if="following.length === 0">팔로잉한 사용자가 없습니다.</li>
        <li v-for="user in following" :key="user.id">
          <a @click="goToUserPage(user.userid)" style="cursor:pointer; color: #145c2b; text-decoration: underline;">
            {{ user.nickname }} ({{ user.userid }})
          </a>
        </li>
      </ul>
    </div>

    <div class="follow-section">
      <h3>팔로워</h3>
      <ul>
        <li v-if="followers.length === 0">팔로워가 없습니다.</li>
        <li v-for="user in followers" :key="user.id">
          <a @click="goToUserPage(user.userid)" style="cursor:pointer; color: #145c2b; text-decoration: underline;">
            {{ user.nickname }} ({{ user.userid }})
          </a>
        </li>
      </ul>
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

// onMounted(async () => {
//   try {
//     const res = await axios.get('http://127.0.0.1:8000/api/v1/users/follow-info/', {
//       headers: {
//         Authorization: `Token ${token}`,
//       }
//     })
//     followers.value = res.data.data.followers
//     following.value = res.data.data.following
//   } catch (err) {
//     console.error('❌ 팔로우 정보 불러오기 실패:', err)
//     alert('팔로우 정보를 불러오는 데 실패했습니다.')
//   }
// })
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
  max-width: 600px;
  margin: auto;
  padding: 2rem;
  font-family: 'Pretendard', sans-serif;
}

.follow-section {
  margin-bottom: 2rem;
}

h2 {
  color: #145c2b;
  text-align: center;
  margin-bottom: 1.5rem;
}

h3 {
  color: #222;
  margin-bottom: 0.8rem;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0.3rem;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}
</style>
