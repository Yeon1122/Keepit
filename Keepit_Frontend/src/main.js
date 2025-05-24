import { createApp } from 'vue'
import { createPinia } from 'pinia'
import '@fortawesome/fontawesome-free/css/all.min.css'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate' // ✅ 설치 후 정상 인식

import App from './App.vue'
import router from './router'

// Import styles
import './assets/styles/variables.css'
import './assets/styles/components.css'

const app = createApp(App)
const pinia = createPinia()

pinia.use(piniaPluginPersistedstate) // ✅ persist 플러그인 등록
app.use(pinia)
app.use(router)

app.mount('#app')
