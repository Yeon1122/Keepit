<template>
  <form @submit.prevent="onLogin">
    <label>아이디:</label>
    <input type="text" v-model="form.userid" />

    <label>비밀번호:</label>
    <input type="password" v-model="form.password" />

    <button type="submit">로그인</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/users.js'

const accountStore = useAccountStore()

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
const onLogin = () => {
  if (!validateForm()) return

  const loginPayload = {
    userid: form.value.userid,
    password: form.value.password
  }

  // const requestData = { ...form.value }
  //   console.log('회원가입 요청 데이터:', requestData)
  accountStore.logIn(loginPayload)
}
</script>

<style scoped>
form {
  background-color: white;
  color: black;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
  margin: auto;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
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
