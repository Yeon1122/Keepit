<template>
  <div class="overlay" @click.self="close">
    <div class="modal">
      <button class="close-btn" @click="close">&times;</button>

      <div v-if="loading" class="loading-state">
        데이터를 불러오는 중입니다...
      </div>

      <div v-else-if="error" class="error-state">
        {{ error }}
      </div>

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
            <div class="stock-info">
              <span class="code">{{ stock.stock_code }}</span>
              <span class="market">{{ stock.market_type }}</span>
            </div>
          </div>
        </div>

        <div class="section">
          <div class="price-info">
            <p class="current-price"><strong>현재가(변동가):</strong> {{ formatNumber(stock.current_price) }}원</p>
            <p class="price-change" :class="({ 'up': stock.price_change > 0, 'down': stock.price_change < 0 })">
              ({{ stock.price_change_str || '-원' }})
            </p>
          </div>
          <p><strong>업종:</strong> {{ stock.sector }}</p>
        </div>

        <div class="section warning" v-if="stock.warning_info">
          <p><strong>⚠️ 주의정보:</strong> {{ stock.warning_info }}</p>
        </div>

        <div class="section">
          <p><strong>시가:</strong> {{ formatNumber(stock.open_price) }}원  <strong>고가:</strong> {{ formatNumber(stock.high_price) }}원  <strong>저가:</strong> {{ formatNumber(stock.low_price) }}원</p>
          <p><strong>52주 최고:</strong> {{ formatNumber(stock.high_52w) }}원 ({{ stock.high_52w_date }})</p>
          <p><strong>52주 최저:</strong> {{ formatNumber(stock.low_52w) }}원 ({{ stock.low_52w_date }})</p>
        </div>

        <div class="section">
          <p><strong>PER:</strong> {{ stock.per }}배 | <strong>PBR:</strong> {{ stock.pbr }}배 | <strong>EPS:</strong> {{ formatNumber(stock.eps) }}원 | <strong>BPS:</strong> {{ formatNumber(stock.bps) }}원</p>
          <p><strong>시가총액:</strong> {{ formatMarketCap(stock.market_cap) }} | <strong>상장 주식 수:</strong> {{ formatNumber(stock.listed_shares) }}주</p>
        </div>

        <div class="section">
          <p><strong>외국인 보유율:</strong> {{ ((stock.foreign_ownership / stock.listed_shares) * 100).toFixed(2) }}%</p>
          <p><strong>공매도 허용:</strong> {{ stock.short_selling_allowed ? '허용' : '불가' }}</p>
        </div>

        <div class="section">
          <h3>관련 뉴스</h3>
          <p v-if="newsList.length === 0" class="empty">관련 뉴스가 없습니다.</p>
          <NewsCard v-else v-for="(news, i) in newsList" :key="i" :news="news" />
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

const close = () => router.back()

const stockCode = route.params.stock_code

const loadStockData = async () => {
  try {
    console.log('주식 데이터 로딩 시작')
    const token = accountStore.token
    const response = await axios.get(
      `http://127.0.0.1:8000/api/v1/products/stocks/${stockCode}/`,
      token ? { headers: { Authorization: `Token ${token}` } } : {}
    )
    console.log('주식 데이터 응답:', response.data)
    stock.value = response.data

    // 찜 여부
    if (isAuthenticated.value) {
      const favRes = await axios.get(
        `http://127.0.0.1:8000/api/v1/products/stocks/${stockCode}/favorite/`,
        { headers: { Authorization: `Token ${accountStore.token}` } }
      )
      isHearted.value = favRes.data.is_liked
      heartCount.value = favRes.data.count
    }

    // 뉴스 데이터 가져오기
    try {
      console.log('뉴스 데이터 요청 시작:', stockCode)
      const newsRes = await axios.get(`http://127.0.0.1:8000/api/v1/news/stock/${stockCode}/`)
      console.log('뉴스 데이터 응답:', newsRes.data)
      if (Array.isArray(newsRes.data)) {
        console.log('뉴스 데이터 개수:', newsRes.data.length)
        newsList.value = newsRes.data
      } else {
        console.error('뉴스 데이터가 배열이 아님:', newsRes.data)
        newsList.value = []
      }
    } catch (newsErr) {
      console.error('뉴스 데이터 로딩 실패:', newsErr.response || newsErr)
      newsList.value = []
    }

  } catch (err) {
    console.error('데이터 로딩 실패:', err.response || err)
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

// 시가총액 포맷팅 (조, 억 단위)
const formatMarketCap = (val) => {
  if (val == null) return '-'
  const num = Number(val)
  if (isNaN(num)) return '-'
  
  // 이미 억 단위로 들어오는 값
  // 1조 = 10000억
  const cho = Math.floor(num / 10000)  // 조 단위
  const uk = num % 10000  // 억 단위 (1조 미만)
  
  if (cho > 0) {
    return uk > 0 ? `${cho.toLocaleString()}조 ${uk.toLocaleString()}억` : `${cho.toLocaleString()}조`
  } else if (uk > 0) {
    return `${uk.toLocaleString()}억`
  } else {
    return '1억 미만'
  }
}
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

.section p,
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
  margin-bottom: 1.5rem;
}

.title-with-heart {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.title-with-heart h2 {
  font-size: 1.8rem;
  margin: 0;
  color: #145c2b;
}

.stock-info {
  display: flex;
  gap: 1rem;
  color: #666;
}

.code, .market {
  font-size: 1rem;
}

.price-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.current-price {
  font-size: 1.2rem;
  margin: 0;
}

.price-change {
  margin: 0;
  &.up { color: #d60000; }
  &.down { color: #0051c7; }
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
