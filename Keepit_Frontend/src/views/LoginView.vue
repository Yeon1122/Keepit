<template>
  <div class="login-container">
    <form @submit.prevent="onLogin">
      <h2>로그인</h2>
      
      <div v-if="route.query.message" class="alert alert-warning">
        {{ route.query.message }}
      </div>

      <label>아이디:</label>
      <input type="text" v-model="form.userid" />

      <label>비밀번호:</label>
      <input type="password" v-model="form.password" />

      <button type="submit">로그인</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/users'
import { useRoute, useRouter } from 'vue-router'

const accountStore = useAccountStore()
const route = useRoute()
const router = useRouter()

const form = ref({
  userid: '',
  password: ''
})

// 유효성 검사
const validateForm = () => {
  if (!form.value.userid || !form.value.password) {
    alert('아이디와 비밀번호를 모두 입력하세요.')
    return false
  }
  return true
}

// 로그인 함수
const onLogin = async () => {
  if (!validateForm()) return

  const loginPayload = {
    userid: form.value.userid,
    password: form.value.password
  }

  // const requestData = { ...form.value }
  //   console.log('회원가입 요청 데이터:', requestData)
  try {
    await accountStore.logIn(loginPayload)
    // 리다이렉트 URL이 있으면 해당 페이지로, 없으면 홈으로 이동
    const redirectPath = route.query.redirect || { name: 'home' }
    router.push(redirectPath)
  } catch (error) {
    console.error('로그인 처리 중 오류:', error)
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 1rem;
}

form {
  background-color: white;
  color: black;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: var(--primary-color);
}

.alert {
  margin-bottom: 1rem;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.alert-warning {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeeba;
}

label {
  display: block;
  margin: 1rem 0 0.25rem;
  font-weight: 600;
}

input {
  width: 100%;
  padding: 0.6rem 0.8rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.95rem;
  background-color: #f9f9f9;
  box-sizing: border-box;
}

button[type="submit"] {
  margin-top: 2rem;
  width: 100%;
  background-color: #145c2b;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  padding: 0.9rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

button[type="submit"]:hover {
  background-color: #0e4a21;
}
</style>