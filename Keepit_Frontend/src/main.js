import { createApp } from 'vue'
import { createPinia } from 'pinia'
import '@fortawesome/fontawesome-free/css/all.min.css'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// Import styles
import './assets/styles/variables.css'
import './assets/styles/components.css'

// axios 기본 설정
axios.defaults.baseURL = 'http://localhost:8000'  // Django 서버 주소

// 요청 인터셉터 설정
axios.interceptors.request.use(
  config => {
    const accountData = JSON.parse(localStorage.getItem('account') || '{}')
    if (accountData.token) {
      config.headers.Authorization = `Token ${accountData.token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 응답 인터셉터 설정
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // 인증 오류 시 로그인 페이지로 리다이렉트
      router.push('/users/login')
    }
    return Promise.reject(error)
  }
)

const app = createApp(App)
const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(router)

app.mount('#app')
