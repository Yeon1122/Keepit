<template>
  <div>
    <div class="title-container">
      <h3>{{ pageTitle }}</h3>

      <!-- 일반 상품 목록일 때의 필터바 -->
      <div v-if="!route.query.userId" class="filter-bar">
        <div class="btn-group">
          <button :class="{ active: selectedType === '정기예금' }" @click="filterByType('정기예금')">정기예금</button>
          <button :class="{ active: selectedType === '적금' }" @click="filterByType('적금')">적금</button>
        </div>

        <select v-model="sortOption" @change="sortProducts">
          <option value="interest">기본금리순</option>
          <option value="special">최고금리순</option>
        </select>
      </div>

      <!-- 찜한 상품 목록일 때의 필터 버튼 -->
      <div v-else class="filter-section">
        <div class="filter-buttons">
          <button 
            class="filter-button" 
            :class="{ active: selectedType === '정기예금' }"
            @click="filterByType('정기예금')"
          >
            예금
          </button>
          <button 
            class="filter-button" 
            :class="{ active: selectedType === '적금' }"
            @click="filterByType('적금')"
          >
            적금
          </button>
        </div>
      </div>
    </div>

    <!-- 일반 상품 목록 -->
    <div v-if="!route.query.userId" class="saving-container">
      <div v-if="loading" class="loading-state">
        {{ loadingMessage }}
      </div>
      <div v-else-if="error" class="error-state">
        {{ error }}
        <button @click="fetchProducts" class="retry-button">다시 시도</button>
      </div>
      <template v-else>
        <SavingCard 
          v-for="product in paginatedProducts" 
          :key="product.id || product.product_code" 
          :product="product" 
          class="saving-card"
        />
        <div v-if="products.length === 0" class="no-data">
          표시할 상품이 없습니다.
        </div>
      </template>
    </div>

    <!-- 찜한 상품 목록 -->
    <div v-else class="products-grid">
      <div v-if="loading" class="loading-state">
        {{ loadingMessage }}
      </div>
      <div v-else-if="error" class="error-state">
        {{ error }}
        <button @click="fetchProducts" class="retry-button">다시 시도</button>
      </div>
      <template v-else>
        <div v-if="paginatedProducts.length" class="products-container">
          <div class="product-card" v-for="product in paginatedProducts" :key="product.id">
            <div class="product-type" :class="product.type">
              {{ product.type === 'deposit' ? '예금' : '적금' }}
            </div>
            <div class="product-content">
              <div class="product-header">
                <div class="company">{{ product.company }}</div>
                <h4 class="product-name">{{ product.name }}</h4>
              </div>
              <div class="product-details">
                <div class="info-row">
                  <span class="label">기본금리</span>
                  <span class="value highlight">{{ product.interest_rate }}%</span>
                </div>
                <div class="info-row">
                  <span class="label">최고금리</span>
                  <span class="value highlight">{{ product.special_rate }}%</span>
                </div>
                <div class="info-row">
                  <span class="label">가입기간</span>
                  <span class="value">{{ product.term }}개월</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <i class="fas fa-heart"></i>
          <p>표시할 상품이 없습니다.</p>
        </div>
      </template>
    </div>

    <div class="pagination" v-if="totalPages > 1">
      <button 
        v-for="page in totalPages" 
        :key="page" 
        @click="goToPage(page)" 
        :class="{ active: page === currentPage }"
      >
        {{ page }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import SavingCard from '@/components/SavingCard.vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/users'
import { useRoute } from 'vue-router'

const route = useRoute()
const loading = ref(true)
const error = ref(null)
const products = ref([])
const selectedType = ref(route.query.type === 'saving' ? '적금' : '정기예금')
const sortOption = ref('interest')
const currentPage = ref(1)
const itemsPerPage = 8
const loadingMessage = ref('데이터를 불러오는 중입니다...')

const accountStore = useAccountStore()
const isAuthenticated = computed(() => accountStore.isAuthenticated)

// 페이지 제목 계산
const pageTitle = computed(() => {
  if (route.query.userId) {
    return `${route.query.nickname}님의 찜한 상품 목록`
  }
  return '정기 예금/적금 상품 안내'
})

const fetchProducts = async () => {
  loading.value = true
  error.value = null
  products.value = []

  try {
    let url
    if (route.query.userId) {
      // 특정 사용자의 찜한 상품 목록을 가져오는 경우
      url = `/api/v1/products/favorites/${route.query.userId}/`
      console.log(`[fetchProducts] 사용자 찜 목록 요청 URL: ${url}`)
      const res = await axios.get(url, {
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      })
      products.value = sortByOption(res.data.filter(product => 
        selectedType.value === '정기예금' ? product.type === 'deposit' : product.type === 'saving'
      ), sortOption.value)
    } else {
      // 전체 상품 목록을 가져오는 경우
      const backendType = selectedType.value === '정기예금' ? 'deposits' : 'savings'
      url = `/api/v1/products/${backendType}/`
      console.log(`[fetchProducts] 전체 상품 요청 URL: ${url}`)
      const res = await axios.get(url)
      
      if (!res.data || (!res.data.data && !Array.isArray(res.data))) {
        throw new Error('데이터 형식이 올바르지 않습니다.')
      }

      const productsData = Array.isArray(res.data) ? res.data : res.data.data
      products.value = sortByOption(productsData.map(product => ({
        ...product,
        type: selectedType.value === '정기예금' ? 'deposit' : 'saving'
      })), sortOption.value)
    }

    currentPage.value = 1
  } catch (err) {
    console.error('[fetchProducts] 오류:', err)
    error.value = '상품 데이터를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

const filterByType = async (type) => {
  selectedType.value = type
  await fetchProducts()
}

const sortProducts = () => {
  products.value = sortByOption([...products.value], sortOption.value)
}

const sortByOption = (list, option) => {
  if (option === 'interest') {
    return [...list].sort((a, b) => b.interest_rate - a.interest_rate)
  } else if (option === 'special') {
    return [...list].sort((a, b) => b.special_rate - a.special_rate)
  }
  return list
}

const totalPages = computed(() => Math.ceil(products.value.length / itemsPerPage))

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return products.value.slice(start, start + itemsPerPage)
})

const goToPage = (page) => {
  currentPage.value = page
}

onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
/* 공통 스타일 */
.title-container {
  padding: 0 2rem;
  margin-top: 2rem;
  margin-bottom: 2rem;
}

h3 {
  color: #145c2b;
  font-weight: bold;
  font-size: 1.5rem;
  margin-left: 1rem;
  margin-bottom: 1.5rem;
  text-align: left;
}

/* 일반 상품 목록 스타일 */
.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding: 0 1rem;
}

.btn-group {
  display: flex;
  gap: 1rem;
}

.btn-group button {
  padding: 0.8rem 2rem;
  border: 2px solid #145c2b;
  background-color: white;
  color: #145c2b;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 8px;
  font-size: 1rem;
}

.btn-group button:hover:not(.active) {
  background-color: #1a703a;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(20, 92, 43, 0.2);
}

.btn-group button.active {
  background-color: #145c2b;
  color: white;
  box-shadow: 0 2px 8px rgba(20, 92, 43, 0.2);
}

select {
  padding: 0.8rem 1.5rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  color: #333;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

select:hover {
  border-color: #145c2b;
}

select:focus {
  outline: none;
  border-color: #145c2b;
  box-shadow: 0 0 0 2px rgba(20, 92, 43, 0.1);
}

.saving-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.saving-card {
  flex: 1 1 300px;
  max-width: 350px;
  min-width: 300px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.saving-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 찜한 상품 목록 스타일 */
.filter-section {
  margin-bottom: 2rem;
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
}

.filter-button {
  padding: 0.5rem 1.5rem;
  border: 1px solid #e0e0e0;
  background: white;
  color: #666;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.filter-button.active {
  background: #145c2b;
  color: white;
  border-color: #145c2b;
}

.products-grid {
  padding: 0 2rem;
}

.products-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.product-card {
  position: relative;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.product-type {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.3rem 1rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.product-type.deposit {
  background: #e3f2fd;
  color: #1976d2;
}

.product-type.saving {
  background: #e8f5e9;
  color: #2e7d32;
}

.product-content {
  padding: 1.5rem;
}

.product-header {
  margin-bottom: 1.5rem;
}

.company {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.product-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin: 0;
  line-height: 1.4;
}

.product-details {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 공통 상태 스타일 */
.loading-state,
.error-state,
.no-data {
  width: 100%;
  text-align: center;
  padding: 3rem;
  color: #666;
  font-size: 1.1rem;
  background-color: #f8f9fa;
  border-radius: 12px;
  margin: 2rem auto;
  max-width: 600px;
}

.error-state {
  color: #dc3545;
  background-color: #fff5f5;
}

.retry-button {
  margin-top: 1.5rem;
  padding: 0.8rem 2rem;
  background-color: #145c2b;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  background-color: #1a703a;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(20, 92, 43, 0.2);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 2rem 0;
  gap: 0.5rem;
}

.pagination button {
  padding: 0.6rem 1rem;
  border: 1px solid #e0e0e0;
  background-color: white;
  color: #145c2b;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 6px;
  min-width: 40px;
}

.pagination button:hover {
  background-color: #f8f9fa;
  border-color: #145c2b;
}

.pagination button.active {
  background-color: #145c2b;
  color: white;
  border-color: #145c2b;
  box-shadow: 0 2px 4px rgba(20, 92, 43, 0.2);
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.empty-state i {
  font-size: 2rem;
  color: #145c2b;
  margin-bottom: 1rem;
}

.empty-state p {
  margin: 0.5rem 0;
  font-size: 1.1rem;
}

.value.highlight {
  color: #145c2b;
  font-weight: 600;
}
</style>
