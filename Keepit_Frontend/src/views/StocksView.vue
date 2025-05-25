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
          v-model="searchKeyword"
          @click="isFocused = true"
          @focus="isFocused = true"
          @blur="() => setTimeout(() => isFocused = false, 100)"
          placeholder="종목명 검색"
        />
        <ul v-if="filteredSuggestions.length && isFocused" class="suggestions">
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
      <div v-if="loading" class="loading-state">
        데이터를 불러오는 중입니다...
      </div>

      <div v-else-if="error" class="error-state">
        {{ error }}
        <button @click="fetchData" class="retry-button">다시 시도</button>
      </div>

      <template v-else>
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
                <span>종목명</span>
              </div>
            </div>
            <div class="price-block">현재가</div>
            <div class="volume-block">거래량 · 거래대금</div>
            <div class="marketcap-block">시가총액</div>
          </div>

          <div class="etf-container">
            <EtfCard
              v-for="etf in etfData"
              :key="etf.etf_code"
              :data="etf"
              :show-heart="isAuthenticated"
            />
          </div>
        </div>
      </template>
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

const searchKeyword = ref('')
const isFocused = ref(false)
const loading = ref(true)
const error = ref(null)

const searchBoxRef = ref(null)

onMounted(async () => {
  document.addEventListener('click', handleClickOutside)
  await fetchData()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

const handleClickOutside = (event) => {
  if (searchBoxRef.value && !searchBoxRef.value.contains(event.target)) {
    isFocused.value = false
  }
}

const fetchData = async () => {
  loading.value = true
  error.value = null
  try {
    if (selectedTab.value === 'stock') {
      const response = await axios.get('http://127.0.0.1:8000/api/v1/products/stocks/')
      stockData.value = response.data
    } else {
      const response = await axios.get('http://127.0.0.1:8000/api/v1/products/etfs/')
      etfData.value = response.data
    }
  } catch (err) {
    console.error('데이터 로딩 실패:', err)
    error.value = '데이터를 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}

const selectTab = async (tab) => {
  selectedTab.value = tab
  searchKeyword.value = ''
  await fetchData()
}

const goToDetail = (stockCode) => {
  router.push({ name: 'stockdetail', params: { stock_code: stockCode } })
}

const onInput = (e) => {
  searchKeyword.value = e.target.value
}

const selectSuggestion = (name) => {
  searchKeyword.value = name
  isFocused.value = false
}

const filteredStockData = computed(() => {
  const keyword = searchKeyword.value.toLowerCase()
  if (!keyword) return stockData.value
  return stockData.value.filter(item =>
    item.name.toLowerCase().includes(keyword)
  )
})

const filteredSuggestions = computed(() => {
  const keyword = searchKeyword.value.toLowerCase()
  if (!keyword) return []
  return stockData.value.filter(item =>
    item.name.toLowerCase().includes(keyword)
  )
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

.loading-state,
.error-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error-state {
  color: #dc3545;
}

.retry-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #145c2b;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.retry-button:hover {
  background-color: #0d4420;
}

.suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
}

.suggestions li {
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.suggestions li:hover {
  background: #f5f5f5;
}

</style>


