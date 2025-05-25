<template>
  <div class="overlay" @click.self="close">
    <div class="modal">
      <button class="close-btn" @click="close">&times;</button>

      <!-- 로딩 상태 -->
      <div v-if="loading" class="loading-state">
        데이터를 불러오는 중입니다...
      </div>

      <!-- 에러 상태 -->
      <div v-else-if="error" class="error-state">
        {{ error }}
      </div>

      <!-- 데이터 표시 -->
      <template v-else-if="stock">
        <div class="header">
          <div class="title-section">
            <div class="title-with-heart">
              <HeartButton
                v-if="isAuthenticated"
                :initial-is-hearted="isHearted"
                :initial-count="heartCount"
                @update:hearted="handleHeart"
              />
              <div v-else class="heart-count">
                찜 {{ heartCount }}개
              </div>
              <h2>{{ stock.name }}</h2>
            </div>
            <span class="code">{{ stock.stock_code }} / {{ stock.market_type }}</span>
          </div>
        </div>
        <div class="section">
          <p><strong>현재가:</strong> {{ formatNumber(stock.current_price) }}원 ({{ formatChange(stock.price_change) }})</p>
          <p><strong>업종:</strong> {{ stock.sector }}</p>
        </div>
        <div class="section warning" v-if="stock.warning_info">
          <p><strong>⚠️ 주의정보:</strong> {{ stock.warning_info }}</p>
        </div>
        <div class="section">
          <p><strong>시가:</strong> {{ formatNumber(stock.open_price) }} / 고가: {{ formatNumber(stock.high_price) }} / 저가: {{ formatNumber(stock.low_price) }}</p>
          <p><strong>52주 최고:</strong> {{ formatNumber(stock.high_52w) }} ({{ stock.high_52w_date }})</p>
          <p><strong>52주 최저:</strong> {{ formatNumber(stock.low_52w) }} ({{ stock.low_52w_date }})</p>
        </div>
        <div class="section">
          <p><strong>PER:</strong> {{ stock.per }} / <strong>PBR:</strong> {{ stock.pbr }} / <strong>EPS:</strong> {{ stock.eps }} / <strong>BPS:</strong> {{ stock.bps }}</p>
          <p><strong>시가총액:</strong> {{ formatNumber(stock.market_cap) }} / <strong>상장주식수:</strong> {{ formatNumber(stock.listed_shares) }}</p>
        </div>
        <div class="section">
          <p><strong>외국인 보유율:</strong> {{ stock.foreign_ownership }}%</p>
          <p><strong>공매도 허용:</strong> {{ stock.short_selling_allowed ? '허용' : '불가' }}</p>
        </div>
        <div class="section">
          <h3>관련 뉴스</h3>
          <NewsCard v-for="(news, i) in newsList" :key="i" :news="news" />
        </div>
      </template>

      <template v-else>
        <p class="empty">데이터가 없습니다.</p>
      </template>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NewsCard from '@/components/NewsCard.vue'
import { useAccountStore } from '@/stores/users'
import HeartButton from '@/components/HeartButton.vue'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()
const stock = ref(null)
const newsList = ref([])
const isAuthenticated = computed(() => accountStore.isAuthenticated)

const isHearted = ref(false)
const heartCount = ref(0)
const loading = ref(true)
const error = ref(null)

const close = () => {
  router.back()
}

const stockCode = route.params.stock_code

const loadStockData = async () => {
  try {
    const token = accountStore.token
    const response = await axios({
      method: 'GET',
      url: `http://127.0.0.1:8000/api/v1/products/stocks/${stockCode}/`,
      headers: token ? {
        Authorization: `Token ${token}`
      } : {}
    })
    stock.value = response.data

    // 찜하기 상태 가져오기
    if (isAuthenticated.value) {
      const favRes = await axios.get(`http://127.0.0.1:8000/api/v1/products/stocks/${stockCode}/favorite/`, {
        headers: { Authorization: `Token ${accountStore.token}` }
      })
      isHearted.value = favRes.data.is_hearted
      heartCount.value = favRes.data.count
    }

    // 뉴스 데이터 가져오기
    const newsRes = await axios.get(`http://127.0.0.1:8000/api/v1/news/stock/${stockCode}/`)
    newsList.value = newsRes.data

  } catch (err) {
    console.error('데이터 로딩 실패:', err)
    error.value = '주식 데이터를 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}

onMounted(loadStockData)

const handleHeart = async (value) => {
  if (!isAuthenticated.value) {
    alert('로그인이 필요한 서비스입니다.')
    return
  }

  try {
    const method = value ? 'POST' : 'DELETE'
    const response = await axios({
      method,
      url: `http://127.0.0.1:8000/api/v1/products/stocks/${stockCode}/favorite/`,
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    
    isHearted.value = value
    heartCount.value = response.data.count
  } catch (err) {
    console.error('찜하기 실패:', err)
    alert('찜하기 처리에 실패했습니다.')
  }
}

const formatNumber = (val) => val == null ? '-' : Number(val).toLocaleString()
const formatChange = (val) => val > 0 ? `+${val}` : val < 0 ? `${val}` : '0'
</script>

<style scoped>
.overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  border: 2px solid #145c2b;
  border-radius: 10px;
  padding: 2rem;
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  font-family: 'Noto Sans KR', sans-serif;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  border: none;
  background: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #333;
}

.header {
  margin-bottom: 1rem;
  color: #333;
}

.section {
  margin-bottom: 1.2rem;
  color: #333;
}

.section p {
  color: #333;
}

.section strong {
  color: #333;
}

.warning {
  background: #fff3cd;
  padding: 0.8rem;
  border-radius: 5px;
  color: #856404;
}

.empty {
  text-align: center;
  padding: 2rem 0;
  color: #999;
  font-size: 1.1rem;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.title-section h2 {
  color: #333;
  margin: 0;
}

.title-with-heart {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.heart-count {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.code {
  color: #666;
  font-size: 0.9rem;
}

.loading-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error-state {
  text-align: center;
  padding: 2rem;
  color: #dc3545;
}
</style>
