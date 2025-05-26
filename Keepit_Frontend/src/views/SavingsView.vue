<template>
  <div>
    <div class="title-container">
      <h3>정기 예금/적금 상품 안내</h3>

      <div class="filter-bar">
        <div class="btn-group">
          <button :class="{ active: selectedType === '정기예금' }" @click="filterByType('정기예금')">정기예금</button>
          <button :class="{ active: selectedType === '적금' }" @click="filterByType('적금')">적금</button>
        </div>

        <select v-model="sortOption" @change="sortProducts">
          <option value="interest">기본금리순</option>
          <option value="special">최고금리순</option>
        </select>
      </div>
    </div>

    <div class="saving-container">
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

    <div class="pagination">
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

const loading = ref(true)
const error = ref(null)
const products = ref([])
const selectedType = ref('정기예금')
const sortOption = ref('interest')
const currentPage = ref(1)
const itemsPerPage = 8
const loadingMessage = ref('데이터를 불러오는 중입니다...')

const accountStore = useAccountStore()
const isAuthenticated = computed(() => accountStore.isAuthenticated)

const fetchProducts = async () => {
  loading.value = true
  error.value = null
  products.value = []

  const backendType = selectedType.value === '정기예금' ? 'deposits' : 'savings'
  const url = `/api/v1/products/${backendType}/`

  try {
    console.log(`[fetchProducts] 요청 URL: ${url}`)
    const res = await axios.get(url)
    
    if (!res.data || (!res.data.data && !Array.isArray(res.data))) {
      throw new Error('데이터 형식이 올바르지 않습니다.')
    }

    const productsData = Array.isArray(res.data) ? res.data : res.data.data
    products.value = sortByOption(productsData.map(product => ({
      ...product,
      type: selectedType.value === '정기예금' ? 'deposit' : 'saving'
    })), sortOption.value)

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
.title-container,
.saving-container {
  padding: 0 2rem;
}

.title-container {
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

/* 필터바 스타일링 */
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

/* 버튼 스타일링 */
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

/* 드롭다운 스타일링 */
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

/* 상품 컨테이너 */
.saving-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* 상품 카드 */
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

/* 로딩, 에러, 데이터 없음 상태 */
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

/* 페이지네이션 */
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
</style>
