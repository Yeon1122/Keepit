<template>
  <div class="favorites-container">
    <div class="favorites-header">
      <h2>찜한 상품 목록</h2>
      <div class="filter-buttons">
        <button 
          class="filter-button" 
          :class="{ active: selectedFilter === 'all' }"
          @click="selectedFilter = 'all'"
        >
          전체
        </button>
        <button 
          class="filter-button" 
          :class="{ active: selectedFilter === 'deposit' }"
          @click="selectedFilter = 'deposit'"
        >
          예금
        </button>
        <button 
          class="filter-button" 
          :class="{ active: selectedFilter === 'saving' }"
          @click="selectedFilter = 'saving'"
        >
          적금
        </button>
        <button 
          class="filter-button" 
          :class="{ active: selectedFilter === 'stock' }"
          @click="selectedFilter = 'stock'"
        >
          주식
        </button>
        <button 
          class="filter-button" 
          :class="{ active: selectedFilter === 'etf' }"
          @click="selectedFilter = 'etf'"
        >
          ETF
        </button>
        <button 
          class="filter-button" 
          :class="{ active: selectedFilter === 'goods' }"
          @click="selectedFilter = 'goods'"
        >
          현물
        </button>
      </div>
    </div>

    <div class="favorites-content">
      <template v-if="filteredProducts.length">
        <ul class="product-list">
          <li v-for="product in filteredProducts" :key="product.id || product.stock_code || product.etf_code" class="product-item">
            <!-- 예금/적금 상품 -->
            <template v-if="product.type === 'deposit' || product.type === 'saving'">
              <div class="product-info-header">
                <span class="product-type">{{ product.type === 'deposit' ? '정기예금' : '적금' }}</span>
                <span class="bank-name">{{ product.company }}</span>
              </div>
              <div class="product-name">{{ product.name }}</div>
              <div class="product-details">
                <div class="rate-info">
                  <span class="label">금리</span>
                  <span class="value">{{ product.interest_rate }}% ~ {{ product.special_rate }}%</span>
                </div>
                <div class="term-info">
                  <span class="label">기간</span>
                  <span class="value">{{ product.term }}개월</span>
                </div>
              </div>
            </template>
            
            <!-- 주식 상품 -->
            <template v-else-if="product.type === 'stock'">
              <div class="product-info-header">
                <span class="product-type">주식</span>
              </div>
              <div class="product-name">{{ product.name }}</div>
              <div class="product-details">
                <div class="price-info">
                  <span class="label">현재가</span>
                  <span class="value">{{ formatPrice(product.current_price) }}원</span>
                </div>
                <div class="change-info">
                  <span class="label">변동가</span>
                  <span class="value" :class="getPriceChangeClass(product.price_change)">
                    <i :class="['fas', product.price_change > 0 ? 'fa-caret-up' : 'fa-caret-down']"></i>
                    {{ formatPriceChange(product.price_change) }}원
                  </span>
                </div>
              </div>
            </template>

            <!-- ETF 상품 -->
            <template v-else-if="product.type === 'etf'">
              <div class="product-info-header">
                <span class="product-type">ETF</span>
                <span class="bank-name">{{ product.company }}</span>
              </div>
              <div class="product-name">{{ product.name }}</div>
              <div class="product-details">
                <div class="price-info">
                  <span class="label">현재가</span>
                  <span class="value">{{ formatPrice(product.current_price) }}원</span>
                </div>
                <div class="change-info">
                  <span class="label">변동가</span>
                  <span class="value" :class="getPriceChangeClass(product.price_change)">
                    <i :class="['fas', product.price_change > 0 ? 'fa-caret-up' : 'fa-caret-down']"></i>
                    {{ formatPriceChange(product.price_change) }}원
                  </span>
                </div>
              </div>
            </template>
            
            <!-- 현물 상품 -->
            <template v-else-if="product.type === 'goods'">
              <div class="product-info-header">
                <span class="product-type">현물</span>
                <span class="bank-name">{{ product.company }}</span>
              </div>
              <div class="product-name">{{ product.name }}</div>
              <div class="product-details">
                <div class="price-info">
                  <span class="label">현재가</span>
                  <span class="value">${{ formatPrice(product.current_price) }} / oz</span>
                </div>
                <div class="change-info">
                  <span class="label">변동가</span>
                  <span class="value" :class="getPriceChangeClass(product.price_change)">
                    <i :class="['fas', product.price_change > 0 ? 'fa-caret-up' : 'fa-caret-down']"></i>
                    ${{ formatPriceChange(product.price_change) }}
                  </span>
                </div>
              </div>
            </template>
          </li>
        </ul>
      </template>
      <div v-else class="empty-state">
        <i class="fas fa-heart"></i>
        <p>{{ getEmptyStateMessage }}</p>
        <p class="sub-text">마음에 드는 상품을 찜해보세요!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/users'
import { useRouter } from 'vue-router'

const accountStore = useAccountStore()
const router = useRouter()

const products = ref([])
const selectedFilter = ref('all')

const filteredProducts = computed(() => {
  if (selectedFilter.value === 'all') {
    return products.value
  }
  return products.value.filter(product => product.type === selectedFilter.value)
})

const getEmptyStateMessage = computed(() => {
  if (selectedFilter.value === 'all') {
    return '아직 찜한 상품이 없습니다.'
  }
  const typeMap = {
    deposit: '예금',
    saving: '적금',
    stock: '주식',
    etf: 'ETF',
    goods: '현물'
  }
  return `찜한 ${typeMap[selectedFilter.value]} 상품이 없습니다.`
})

onMounted(async () => {
  const token = accountStore.token
  if (!token) {
    alert('로그인이 필요한 서비스입니다.')
    router.push('/login')
    return
  }

  try {
    const response = await axios.get('/api/v1/products/favorites/', {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    products.value = response.data
  } catch (error) {
    console.error('찜한 상품 목록 로딩 실패:', error)
    alert('찜한 상품 목록을 불러오는데 실패했습니다.')
  }
})

// 가격 포맷팅 함수 추가
const formatPrice = (price) => {
  if (!price) return '0'
  return price.toLocaleString()
}

// 가격 변동 포맷팅 함수 추가
const formatPriceChange = (change) => {
  if (!change) return '0'
  return Math.abs(change).toLocaleString()
}

// 가격 변동에 따른 클래스 반환 함수 추가
const getPriceChangeClass = (change) => {
  if (!change) return ''
  return change > 0 ? 'price-up' : 'price-down'
}
</script>

<style scoped>
.favorites-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.favorites-header {
  margin-bottom: 2rem;
}

.favorites-header h2 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1rem;
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.filter-button {
  padding: 0.4rem 1rem;
  border: 1px solid #dee2e6;
  border-radius: 20px;
  background: white;
  color: #495057;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.filter-button:hover {
  background: #f8f9fa;
}

.filter-button.active {
  background: #145c2b;
  color: white;
  border-color: #145c2b;
}

.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  list-style: none;
  padding: 0;
  margin: 0;
}

.product-item {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s ease;
}

.product-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.product-info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.product-type {
  background-color: #145c2b;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.bank-name {
  color: #666;
  font-size: 0.9rem;
}

.product-name {
  font-weight: bold;
  margin: 0.5rem 0;
  font-size: 1.1rem;
  color: #333;
}

.product-details {
  display: grid;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.rate-info,
.term-info,
.price-info,
.change-info,
.volume-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  color: #666;
  font-size: 0.9rem;
}

.value {
  font-weight: 600;
  color: #145c2b;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
}

.empty-state i {
  font-size: 2.5rem;
  color: #145c2b;
  margin-bottom: 1rem;
}

.empty-state p {
  margin: 0.5rem 0;
  color: #666;
}

.empty-state .sub-text {
  font-size: 0.9rem;
  color: #999;
}

@media (max-width: 768px) {
  .filter-buttons {
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }

  .filter-button {
    white-space: nowrap;
  }

  .product-list {
    grid-template-columns: 1fr;
  }
}

.price-up {
  color: #d63031;
  display: flex;
  align-items: center;
  gap: 0.2rem;
}

.price-down {
  color: #0984e3;
  display: flex;
  align-items: center;
  gap: 0.2rem;
}

.price-up i,
.price-down i {
  font-size: 1.2rem;
}
</style> 