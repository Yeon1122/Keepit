<template>
  <div>
    <div class="title-container">
    <h3>주식/ETF 상품 안내</h3>

    <div class="top-row">
      <div class="btn-group">
        <button :class="{ active: selectedTab === 'stock' }" @click="selectTab('stock')">주식</button>
        <button :class="{ active: selectedTab === 'etf' }" @click="selectTab('etf')">ETF</button>
      </div>

      <div v-if="selectedTab === 'stock'" class="search-box" ref="searchBoxRef">
        <input
          type="text"
          :value="searchKeyword"
          @input="onInput"
          @click="isFocused = true"
          @focus="isFocused = true"
          @blur="() => setTimeout(() => isFocused = false, 100)"
          placeholder="종목명 검색"
        />
        <ul v-if="filteredSuggestions.length && isFocused">
          <li
            v-for="suggestion in filteredSuggestions"
            :key="suggestion.id"
            @click="selectSuggestion(suggestion.name)"
          >
            {{ suggestion.name }}
          </li>
        </ul>
      </div>
    </div>
  </div>

    <div class="content-container">
      <div class="stock-content" v-if="selectedTab === 'stock'">
        <div class="header-row">
          <div class="left">
            <div class="info">
              <div v-if="isAuthenticated" class="heart-space"></div>
              <span>종목</span>
            </div>
          </div>
          <div class="price-block">현재가</div>
          <div class="volume-block">누적 거래량 · 대금</div>
          <div class="marketcap-block">시가총액</div>
        </div>

        <div class="stock-container">

          <StockCard
            v-for="item in filteredStockData"
            :key="item.id"
            :data="item"
            :show-heart="isAuthenticated"
            @click="goToDetail(item.stock_code)"
          />
        </div>
      </div>

      <div class="etf-content" v-if="selectedTab === 'etf'">
        <div class="header-row">
          <div class="left">
            <div class="info">
              <div v-if="isAuthenticated" class="heart-space"></div>
              <span>종목 · 업종</span>
            </div>
          </div>
          <div class="price-block">현재가</div>
          <div class="marketcap-block">NAV</div>
        </div>

        <div class="etf-container">
          <EtfCard
            v-for="etf in etfData"
            :key="etf.id"
            :data="etf"
            :show-heart="isAuthenticated"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import StockCard from '@/components/StockCard.vue'
import EtfCard from '@/components/EtfCard.vue'
import { useAccountStore } from '@/stores/users'

const selectedTab = ref('stock')
const stockData = ref([])
const etfData = ref([])
const router = useRouter()
const accountStore = useAccountStore()
const isAuthenticated = computed(() => accountStore.isAuthenticated)

const searchKeyword = ref('') // 🔧 추가됨
const isFocused = ref(false)

const searchBoxRef = ref(null) // 🔧 DOM 참조

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

const handleClickOutside = (event) => {
  if (searchBoxRef.value && !searchBoxRef.value.contains(event.target)) {
    isFocused.value = false
  }
}

const selectTab = (tab) => {
  selectedTab.value = tab
  searchKeyword.value = '' // 🔧 검색어 초기화
}

const goToDetail = (stockCode) => {
  router.push({ name: 'stockdetail', params: { stock_code: stockCode } })
}

// 🔧 input 이벤트 핸들러
const onInput = (e) => {
  searchKeyword.value = e.target.value
}

// 🔧 자동완성 클릭 시 값 지정
const selectSuggestion = (name) => {
  searchKeyword.value = name
  isFocused.value = false
}


// 🔧 필터링된 주식 목록
const filteredStockData = computed(() => {
  const keyword = searchKeyword.value.toLowerCase()
  if (!keyword) return stockData.value
  return stockData.value.filter(item =>
    item.name.toLowerCase().includes(keyword)
  )
})

// 🔧 자동완성 후보
const filteredSuggestions = computed(() => {
  const keyword = searchKeyword.value.toLowerCase()
  if (!keyword) return []
  return stockData.value.filter(item =>
    item.name.toLowerCase().includes(keyword)
  )
})

onMounted(() => {
  stockData.value = [
    {
      id: 1,
      type: 'stock',
      name: '삼성전자',
      stock_code: '005930',
      current_price: 68800,
      base_price: 68900,
      market_cap: 412500000000000,
      trade_volume: 10500000,
      trade_value: 721000000000
    },
    {
      id: 2,
      type: 'stock',
      name: '카카오',
      stock_code: '035720',
      current_price: 56000,
      base_price: 55000,
      market_cap: 42300000000000,
      trade_volume: 1800000,
      trade_value: 98700000000
    }
  ]

  etfData.value = [
    {
      id: 1,
      type: 'etf',
      name: 'KODEX 200',
      current_price: 39350,
      price_change: 150,
      sector: '지수',
      nav: 39380,
      nav_change: 120
    },
    {
      id: 2,
      type: 'etf',
      name: 'TIGER 미국S&P500',
      current_price: 103050,
      price_change: -200,
      sector: '해외지수',
      nav: 103000,
      nav_change: -150
    }
  ]
})
</script>

<style scoped>
.title-container,
.content-container {
  padding: 0 2rem;
}

.title-container {
  margin-top: 1.5rem;
  position: relative;
}

h3 {
  color: #145c2b;
  font-weight: bold;
  font-size: 1.3rem;
  margin-bottom: 1rem;
}

.btn-group {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

button {
  padding: 0.6rem 1.5rem;
  border: 2px solid #145c2b;
  background-color: white;
  color: #145c2b;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
}

button:hover:not(.active) {
  background-color: #145c2b;
  color: white;
}

button.active {
  background-color: #145c2b;
  color: white;
}

.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #145c2b;
  padding: 0.8rem 1.5rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  font-weight: bold;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.header-row * {
  color: white;
}

.header-row > .left {
  flex: 2;
  text-align: left;
}

.header-row > .left .info {
  display: flex;
  align-items: center;
  gap: 0.7rem;
}

.header-row > .left .heart-space {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.stock-content .price-block {
  flex: 1.5;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.etf-content .price-block {
  flex: 0.75;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.stock-content .volume-block {
  flex: 1.25;
  align-items: flex-end;
  text-align: center;
}

.etf-content .volume-block {
  flex: 2.75;
  text-align: center;
}

.header-row > .marketcap-block {
  flex: 0.75;
  text-align: right;
}

.stock-container,
.etf-container {
  max-width: 1200px;
  margin: 0 auto;
}

.top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.search-box {
  width: 240px;
  position: relative;
}

.search-box input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
}

.search-box ul {
  list-style: none;
  margin: 0;
  padding: 0.5rem;
  position: absolute;
  background: white;
  border: 1px solid #ccc;
  border-radius: 6px;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
}

.search-box li {
  padding: 0.3rem 0.5rem;
  cursor: pointer;
}

.search-box li:hover {
  background-color: #f0f0f0;
}

</style>


