<template>
  <div>
    <div class="title-container">
    <h3>정기 예금/적금 상품 안내</h3>

    <div class="btn-group">
        <button
            :class="{ active: selectedType === '예금' }"
            @click="filterByType('예금')"
        >예금</button>

        <button
            :class="{ active: selectedType === '적금' }"
            @click="filterByType('적금')"
        >적금</button>
    </div>
    </div>
    <div class="saving-container">
      <SavingCard
        v-for="product in products"
        :key="product.id"
        :product="product"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import SavingCard from '@/components/SavingCard.vue'
import axios from 'axios'

const allProducts = ref([])
const products = ref([])

onMounted(() => {
  allProducts.value = [
    {
      id: 1,
      type: "정기예금",
      name: "국민 튼튼예금",
      company: "국민은행",
      interest_rate: 3.2,
      special_rate: 3.8,
      term: 12,
      target: "만 19세 이상 개인"
    },
    {
      id: 2,
      type: "적금",
      name: "삼성전자",
      company: "삼성전자",
      stock_code: "005930",
      market_type: "KOSPI",
      current_price: 76000,
      price_change: -300
    }
  ]
  filterByType(selectedType.value)
})

// onMounted(async () => {
//   try {
//     const res = await axios.get('/api/v1/products/savings/')
//     allProducts.value = res.data.data  // 백엔드 응답 구조에 따라 조정
//     filterByType(selectedType.value)   // ✅ 선택된 유형으로 필터링
//   } catch (err) {
//     console.error('❌ 상품 데이터를 불러오는 데 실패했습니다.', err)
//   }
// })

const selectedType = ref('예금')

const filterByType = (type) => {
  selectedType.value = type
  if (type === '예금') {
    products.value = allProducts.value.filter(p => p.id === 1)
  } else if (type === '적금') {
    products.value = allProducts.value.filter(p => p.id === 2)
  }
}
</script>

<style scoped>
.title-container,
.saving-container {
  padding: 0 2rem;
}

.title-container {
  margin-top: 1.5rem;
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

/* 기본 상태 */
button {
  padding: 0.6rem 1.5rem;
  border: 2px solid #145c2b;
  background-color: white;
  color: #145c2b;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
}

/* hover일 때만 적용되도록 명확히 지정 */
button:hover:not(.active) {
  background-color: #145c2b;
  color: white;
}

/* 선택된 버튼 */
button.active {
  background-color: #145c2b;
  color: white;
}

</style>
