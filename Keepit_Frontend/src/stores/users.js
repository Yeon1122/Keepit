import { ref, watch } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const router = useRouter()

  // 상태 변수
  const token = ref('')
  const userId = ref(null)
  const isAuthenticated = ref(false)

  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/api/v1/users'

   const applyTokenToAxios = () => {
    if (token.value) {
      axios.defaults.headers.common['Authorization'] = `Token ${token.value}`
    } else {
      delete axios.defaults.headers.common['Authorization']
    }
  }

  // ✅ token이 변할 때마다 axios에 적용
  watch(token, () => {
    applyTokenToAxios()
  }, { immediate: true })

  // ✅ 회원가입
  const signUp = async (payload) => {
    try {
      const res = await axios.post(`${ACCOUNT_API_URL}/signup/`, {
        userid: payload.userid,
        password: payload.password,
        name: payload.name,
        nickname: payload.nickname,
        email: payload.email,
        birth_year: Number(payload.birthYear),
        birth_month: Number(payload.birthMonth),
        birth_day: Number(payload.birthDay),
        income_range: payload.incomeRange,
        region_city: payload.regionCity,
        region_district: payload.regionDistrict,
      })

      alert('✅ 회원가입이 완료되었습니다.')
      console.log('회원가입 응답:', res.data)
      router.push({ name: 'login' })  // 또는 회원가입 후 자동 로그인 시 home
    } catch (err) {
      console.error('❌ 회원가입 실패:', err.response?.data || err.message)
      alert('회원가입에 실패했습니다.')
    }
  }

  // ✅ 로그인
  const logIn = async (payload) => {
    try {
      const res = await axios.post(`${ACCOUNT_API_URL}/login/`, {
        userid: payload.userid,
        password: payload.password,
      })

      token.value = res.data.token
      userId.value = res.data.user_id
      isAuthenticated.value = true

      console.log('✅ 로그인 성공')
      router.push({ name: 'home' })
    } catch (err) {
      console.error('❌ 로그인 실패:', err.response?.data || err.message)
      alert('로그인 실패! 아이디/비밀번호를 확인하세요.')
    }
  }

  

  // ✅ 로그아웃
  const logOut = async () => {
    try {
      await axios.delete('/api/v1/users/logout/', {
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      console.log('✅ 서버 로그아웃 요청 완료')
    } catch (error) {
      console.error('❌ 서버 로그아웃 실패:', error.response?.data || error.message)
    }

    // 프론트 상태 초기화
    token.value = ''
    userId.value = null
    isAuthenticated.value = false
    router.push({ name: 'home' })
  }

  return {
    token,
    userId,
    isAuthenticated,
    signUp,
    logIn,
    logOut,
  }
}, { persist: true })


