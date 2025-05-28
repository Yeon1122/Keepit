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
          @input="(e) => searchKeyword = e.target.value"
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
      <div v-if="loading" class="loading-overlay">
        <lottie-player
          :animationData="loadingAnimation"
          :loop="true"
          :autoplay="true"
          style="width: 200px; height: 200px;"
        />
        <p class="loading-text">{{ selectedTab === 'stock' ? '주식' : 'ETF' }} 데이터를 불러오는 중입니다...</p>
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
            <div v-if="loadingMore" class="loading-more">
              추가 데이터를 불러오는 중입니다...
            </div>
            <div v-if="!loadingMore && hasMoreStock" class="load-more-button" @click="loadMore">
              더 보기
            </div>
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
            <div class="volume-block">거래량</div>
            <div class="trade-value-block">거래대금</div>
            <div class="marketcap-block">시가총액</div>
          </div>

          <div class="etf-container">
            <EtfCard
              v-for="etf in etfData"
              :key="etf.etf_code"
              :data="etf"
              :show-heart="isAuthenticated"
            />
            <div v-if="loadingMore" class="loading-more">
              추가 데이터를 불러오는 중입니다...
            </div>
            <div v-if="!loadingMore && hasMoreEtf" class="load-more-button" @click="loadMore">
              더 보기
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import StockCard from '@/components/StockCard.vue'
import EtfCard from '@/components/EtfCard.vue'
import { useAccountStore } from '@/stores/users'
import loadingAnimation from '@/assets/animations/stock_loading.json'
import LottiePlayer from '@/components/LottiePlayer.vue'

const router = useRouter()
const route = useRoute()
const accountStore = useAccountStore()
const isAuthenticated = computed(() => accountStore.isAuthenticated)

const selectedTab = ref(route.query.type === 'etf' ? 'etf' : 'stock')
const stockData = ref([])
const etfData = ref([])

const searchKeyword = ref('')
const isFocused = ref(false)
const loading = ref(false)
const error = ref(null)

// 페이지네이션 관련 상태
const pageSize = ref(50)  // 한 번에 불러올 개수를 50개로 설정
const stockPage = ref(1)
const etfPage = ref(1)
const hasMoreStock = ref(true)
const hasMoreEtf = ref(true)
const loadingMore = ref(false)

const searchBoxRef = ref(null)

onMounted(async () => {
  document.addEventListener('click', handleClickOutside)
  if (selectedTab.value === 'stock') {
    await fetchStockData()
  } else {
    await fetchETFData()
  }
  
  const container = document.querySelector(
    selectedTab.value === 'stock' ? '.stock-container' : '.etf-container'
  )
  if (container) {
    container.addEventListener('scroll', handleScroll)
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  const container = document.querySelector(
    selectedTab.value === 'stock' ? '.stock-container' : '.etf-container'
  )
  if (container) {
    container.removeEventListener('scroll', handleScroll)
  }
})

const handleClickOutside = (event) => {
  if (searchBoxRef.value && !searchBoxRef.value.contains(event.target)) {
    isFocused.value = false
  }
}

const fetchStockData = async (isLoadMore = false) => {
  if (!isLoadMore) {
    loading.value = true
  } else {
    loadingMore.value = true
  }
  error.value = null

  try {
    const headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
    const response = await axios.get('http://127.0.0.1:8000/api/v1/products/stocks/', {
      headers,
      params: {
        page: stockPage.value,
        size: pageSize.value
      }
    })
    
    if (isLoadMore) {
      stockData.value = [...stockData.value, ...response.data.data]
    } else {
      stockData.value = response.data.data
    }
    
    hasMoreStock.value = response.data.has_more
    if (response.data.has_more) {
      stockPage.value += 1
    }
  } catch (err) {
    console.error('주식 데이터 로딩 실패:', err)
    error.value = '데이터를 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

const fetchETFData = async (isLoadMore = false) => {
  if (!isLoadMore) {
    loading.value = true
  } else {
    loadingMore.value = true
  }
  error.value = null

  try {
    const headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/products/etfs/`, {
      headers,
      params: {
        page: etfPage.value,
        size: pageSize.value
      }
    })
    
    if (isLoadMore) {
      etfData.value = [...etfData.value, ...response.data.data]
    } else {
      etfData.value = response.data.data
    }
    
    hasMoreEtf.value = response.data.has_more
    if (response.data.has_more) {
      etfPage.value += 1
    }
  } catch (err) {
    console.error('ETF 데이터 로딩 실패:', err)
    error.value = '데이터를 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

const selectTab = async (tab) => {
  selectedTab.value = tab
  searchKeyword.value = ''
  
  // 탭 변경 시 스크롤 이벤트 리스너 재설정
  const oldContainer = document.querySelector(
    tab === 'stock' ? '.etf-container' : '.stock-container'
  )
  if (oldContainer) {
    oldContainer.removeEventListener('scroll', handleScroll)
  }
  
  // 새로운 탭의 데이터가 없을 때만 로드
  if (tab === 'stock' && stockData.value.length === 0) {
    stockPage.value = 1
    await fetchStockData()
  } else if (tab === 'etf' && etfData.value.length === 0) {
    etfPage.value = 1
    await fetchETFData()
  }
  
  // 새 탭의 스크롤 이벤트 리스너 설정
  const newContainer = document.querySelector(
    tab === 'stock' ? '.stock-container' : '.etf-container'
  )
  if (newContainer) {
    newContainer.addEventListener('scroll', handleScroll)
  }
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

const loadMore = async () => {
  if (loadingMore.value) return
  
  if (selectedTab.value === 'stock' && hasMoreStock.value) {
    await fetchStockData(true)
  } else if (selectedTab.value === 'etf' && hasMoreEtf.value) {
    await fetchETFData(true)
  }
}

const handleScroll = () => {
  const container = selectedTab.value === 'stock' 
    ? document.querySelector('.stock-container')
    : document.querySelector('.etf-container')
    
  if (!container) return

  const { scrollTop, scrollHeight, clientHeight } = container
  if (scrollTop + clientHeight >= scrollHeight - 100) {
    loadMore()
  }
}

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
  min-width: 200px;
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
  flex: 1;
  text-align: right;
  min-width: 120px;
}

.etf-content .price-block {
  flex: 1;
  text-align: right;
  min-width: 120px;
}

.stock-content .volume-block {
  flex: 1.5;
  text-align: right;
  min-width: 200px;
  padding-right: 10px;
  margin-right: -15px;
}

.etf-content .volume-block {
  flex: 1;
  text-align: right;
  min-width: 120px;
  padding-right: 10px;
  margin-right: -15px;
}

.etf-content .trade-value-block {
  flex: 1;
  text-align: right;
  min-width: 120px;
  padding-right: 10px;
  margin-right: -15px;
}

.stock-content .marketcap-block {
  flex: 1;
  text-align: right;
  min-width: 120px;
  padding-right: 10px;
}

.etf-content .marketcap-block {
  flex: 1;
  text-align: right;
  min-width: 120px;
  padding-right: 10px;
}

.stock-container,
.etf-container {
  max-width: 1200px;
  margin: 0 auto;
  max-height: 800px;
  overflow-y: auto;
  padding-right: 10px;
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

.loading-state {
  text-align: center;
  padding: 2rem;
  color: #145c2b;
  font-weight: bold;
  font-size: 1.1rem;
}

.loading-text {
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-more {
  text-align: center;
  padding: 1rem;
  color: #666;
}

.load-more-button {
  text-align: center;
  padding: 1rem;
  background-color: #f5f5f5;
  cursor: pointer;
  margin: 1rem 0;
  border-radius: 8px;
  color: #145c2b;
  font-weight: bold;
}

.load-more-button:hover {
  background-color: #e0e0e0;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-text {
  margin-top: 1rem;
  font-size: 1.1rem;
  color: #666;
}

</style>


