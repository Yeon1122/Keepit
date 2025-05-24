import { ref, watch } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const router = useRouter()

  // 상태 변수들을 세션 스토리지에서 초기화
  const token = ref(sessionStorage.getItem('token') || '')
  const user_id = ref(sessionStorage.getItem('user_id') || '')
  const userId = ref(sessionStorage.getItem('userId') || null)
  const isAuthenticated = ref(!!sessionStorage.getItem('token'))

  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/api/v1/users'

  // axios 인터셉터 설정
  axios.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response) {
        switch (error.response.status) {
          case 401: // 인증 실패
            // 토큰이 만료되었거나 유효하지 않은 경우
            logOut()
            router.push({
              name: 'login',
              query: {
                redirect: router.currentRoute.value.fullPath,
                message: '로그인이 필요하거나 인증이 만료되었습니다.'
              }
            })
            break
          case 403: // 권한 없음
            alert('해당 작업에 대한 권한이 없습니다.')
            break
          case 404: // 리소스 없음
            router.push({ name: 'home' })
            break
        }
      }
      return Promise.reject(error)
    }
  )

  // axios 요청 인터셉터 추가
  axios.interceptors.request.use(
    (config) => {
      const token = sessionStorage.getItem('token')
      if (token) {
        config.headers.Authorization = `Token ${token}`
      }
      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

  const applyTokenToAxios = () => {
    if (token.value) {
      axios.defaults.headers.common['Authorization'] = `Token ${token.value}`
      // 토큰을 세션 스토리지에 저장
      sessionStorage.setItem('token', token.value)
    } else {
      delete axios.defaults.headers.common['Authorization']
      // 토큰 제거
      sessionStorage.removeItem('token')
    }
  }

  // token이 변할 때마다 axios에 적용
  watch(token, () => {
    applyTokenToAxios()
  }, { immediate: true })

  // user_id 변경 감시
  watch(user_id, (newValue) => {
    if (newValue) {
      sessionStorage.setItem('user_id', newValue)
    } else {
      sessionStorage.removeItem('user_id')
    }
  })

  // userId 변경 감시
  watch(userId, (newValue) => {
    if (newValue) {
      sessionStorage.setItem('userId', newValue)
    } else {
      sessionStorage.removeItem('userId')
    }
  })

  // 회원가입
  const signUp = async (payload) => {
    try {
      const requestData = {
        userid: payload.userid,
        password: payload.password,
        name: payload.name,
        nickname: payload.nickname,
        email: payload.email,
        birth_year: Number(payload.birthYear),
        birth_month: Number(payload.birthMonth),
        birth_day: Number(payload.birthDay),
        region_city: payload.regionCity,
        region_district: payload.regionDistrict,
      }

      console.log('회원가입 요청 URL:', `${ACCOUNT_API_URL}/signup/`)
      console.log('회원가입 요청 데이터:', requestData)

      const res = await axios.post(`${ACCOUNT_API_URL}/signup/`, requestData)

      alert('✅ 회원가입이 완료되었습니다.')
      router.push({ name: 'login' })
    } catch (err) {
      console.error('❌ 회원가입 실패:', err.response?.data || err.message)
      if (err.response?.data) {
        console.log('서버 응답 데이터:', err.response.data)
      }
      alert('회원가입에 실패했습니다. 입력하신 정보를 다시 확인해주세요.')
    }
  }

  // 로그인
  const logIn = async (payload) => {
    try {
      const res = await axios.post(`${ACCOUNT_API_URL}/login/`, {
        userid: payload.userid,
        password: payload.password,
      })

      user_id.value = res.data.user_id
      token.value = res.data.token
      userId.value = payload.userid
      isAuthenticated.value = true

      console.log('✅ 로그인 성공')
      router.push({ name: 'home' })
    } catch (err) {
      console.error('❌ 로그인 실패:', err.response?.data || err.message)
      alert('로그인 실패! 아이디/비밀번호를 확인하세요.')
    }
  }

  // 로그아웃
  const logOut = async () => {
    try {
      if (token.value) {
        await axios.delete(`${ACCOUNT_API_URL}/logout/`, {
          headers: {
            Authorization: `Token ${token.value}`
          }
        })
        console.log('✅ 서버 로그아웃 요청 완료')
      }
    } catch (error) {
      console.error('❌ 서버 로그아웃 실패:', error.response?.data || error.message)
    } finally {
      // 상태 및 스토리지 초기화
      token.value = ''
      user_id.value = null
      userId.value = null
      isAuthenticated.value = false

      // 세션 스토리지 클리어
      sessionStorage.clear()

      // axios 헤더 제거
      delete axios.defaults.headers.common['Authorization']

      router.push({ name: 'home' })
    }
  }

  return {
    token,
    user_id,
    userId,
    isAuthenticated,
    signUp,
    logIn,
    logOut,
  }
})


