<template>
  <div class="overlay" @click.self="close">
    <div class="modal">
      <button class="close-btn" @click="close">&times;</button>
      <template v-if="stock">
        <div class="header">
          <h2>{{ stock.name }}</h2>
          <p>{{ stock.stock_code }} / {{ stock.market_type }}</p>
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
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NewsCard from '@/components/NewsCard.vue'

const route = useRoute()
const router = useRouter()
const stock = ref(null)
const newsList = ref([])

const close = () => {
  router.back()
}

onMounted(() => {
  const dummyStockData = {
    '005930': {
      name: '삼성전자', stock_code: '005930', market_type: 'KOSPI', current_price: 68800,
      price_change: -100, sector: '전자', warning_info: '', open_price: 69000, high_price: 69200,
      low_price: 68500, high_52w: 80000, high_52w_date: '2024-11-01', low_52w: 58000, low_52w_date: '2024-03-01',
      per: 10.5, pbr: 1.3, eps: 6500, bps: 52000, market_cap: 412500000000000, listed_shares: 600000000,
      foreign_ownership: 55.3, short_selling_allowed: true
    },
    '035720': {
      name: '카카오', stock_code: '035720', market_type: 'KOSPI', current_price: 56000,
      price_change: -200, sector: '인터넷', warning_info: '투자주의 종목', open_price: 55200, high_price: 55500,
      low_price: 54600, high_52w: 70000, high_52w_date: '2024-10-01', low_52w: 50000, low_52w_date: '2024-01-01',
      per: 35.2, pbr: 2.1, eps: 1600, bps: 26400, market_cap: 42300000000000, listed_shares: 880000000,
      foreign_ownership: 32.8, short_selling_allowed: false
    }
  }

  const dummyNews = [
    { title: '삼성전자, 2분기 실적 발표…전망은?', url: 'https://news.example.com/1', date: '2025.05.21' },
    { title: '카카오, 신사업 확장으로 주가 상승 기대', url: 'https://news.example.com/2', date: '2025.05.20' },
    { title: 'IT 업계 하반기 투자 전략은?', url: 'https://news.example.com/3', date: '2025.05.19' }
  ]

  const code = route.params.stock_code
  stock.value = dummyStockData[code] || null
  newsList.value = dummyNews

  // 실제 API 요청 (백엔드 연결 시 사용 예정)
  // try {
  //   const res = await axios.get(`http://127.0.0.1:8000/api/v1/products/stocks/${code}`)
  //   stock.value = res.data
  // } catch (e) {
  //   stock.value = null
  // }
})

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
}

.header {
  margin-bottom: 1rem;
}

.section {
  margin-bottom: 1.2rem;
}

.warning {
  background: #fff3cd;
  padding: 0.8rem;
  border-radius: 5px;
}

.empty {
  text-align: center;
  padding: 2rem 0;
  color: #999;
  font-size: 1.1rem;
}
</style>
