import { ref, watch } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const router = useRouter()

  // localStorage에서 account 정보 가져오기
  const accountData = JSON.parse(localStorage.getItem('account') || '{}')

  // 상태 변수들을 account 데이터에서 초기화
  const token = ref(accountData.token || '')
  const user_id = ref(accountData.user_id || '')
  const userId = ref(accountData.userId || '')
  const isAuthenticated = ref(accountData.isAuthenticated || false)

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
      const accountData = JSON.parse(localStorage.getItem('account') || '{}')
      if (accountData.token) {
        config.headers.Authorization = `Token ${accountData.token}`
      }
      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

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

      // 회원가입 성공시에만 로그인 페이지로 이동
      if (res.data) {
        alert('✅ 회원가입이 완료되었습니다.')
        router.push({ name: 'login' })
        return true
      }
      return false
    } catch (err) {
      console.error('❌ 회원가입 실패:', err.response?.data || err.message)

      // 서버 응답에서 구체적인 에러 메시지 확인
      if (err.response?.data) {
        const errorData = err.response.data
        if (errorData.userid) {
          alert('이미 사용 중인 아이디입니다. 다른 아이디를 선택해주세요.')
        } else if (errorData.email) {
          alert('이미 등록된 이메일입니다. 다른 이메일을 사용해주세요.')
        } else if (errorData.nickname) {
          alert('이미 사용 중인 닉네임입니다. 다른 닉네임을 선택해주세요.')
        } else {
          alert('회원가입에 실패했습니다. 입력하신 정보를 다시 확인해주세요.')
        }
        console.log('서버 응답 데이터:', errorData)
      } else {
        alert('회원가입에 실패했습니다. 잠시 후 다시 시도해주세요.')
      }
      return false
    }
  }

  // 로그인
  const logIn = async (payload) => {
    try {
      const res = await axios.post(`${ACCOUNT_API_URL}/login/`, {
        userid: payload.userid,
        password: payload.password,
      })

      // 필수 정보만 저장
      const essentialData = {
        token: res.data.token,
        user_id: res.data.user_id,
        userId: payload.userid,
        isAuthenticated: true
      }

      // store의 상태 업데이트
      token.value = res.data.token
      user_id.value = res.data.user_id
      userId.value = payload.userid
      isAuthenticated.value = true

      // localStorage에 저장
      localStorage.setItem('account', JSON.stringify(essentialData))

      // axios 헤더 설정
      axios.defaults.headers.common['Authorization'] = `Token ${res.data.token}`

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
      // 상태 초기화
      token.value = ''
      user_id.value = ''
      userId.value = ''
      isAuthenticated.value = false

      // localStorage에서 모든 인증 관련 데이터 제거
      localStorage.removeItem('account')
      localStorage.removeItem('token')
      localStorage.removeItem('user_id')
      localStorage.removeItem('userId')

      // axios 헤더 제거
      delete axios.defaults.headers.common['Authorization']

      // 홈으로 이동
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
    logOut
  }
})


