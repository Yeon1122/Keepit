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
axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.withCredentials = false

const app = createApp(App)
const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(router)

app.mount('#app')
