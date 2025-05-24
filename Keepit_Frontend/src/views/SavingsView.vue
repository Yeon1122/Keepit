<template>
  <div>
    <div class="title-container">
      <h3>정기 예금/적금 상품 안내</h3>

      <!-- ✅ 왼쪽 버튼 + 오른쪽 드롭다운 정렬 -->
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
      <SavingCard v-for="product in paginatedProducts" :key="product.id" :product="product" class="saving-card" />
    </div>

    <div class="pagination">
      <button v-for="page in totalPages" :key="page" @click="goToPage(page)" :class="{ active: page === currentPage }">
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
import HeartButton from '@/components/HeartButton.vue'

const allProducts = ref([])
const products = ref([])

const selectedType = ref('정기예금')
const sortOption = ref('interest')

const currentPage = ref(1)
const itemsPerPage = 8

const accountStore = useAccountStore()
const isAuthenticated = computed(() => accountStore.isAuthenticated)

// onMounted(async () => {
//   try {
//     const res = await axios.get('http://127.0.0.1:8000/api/v1/products/savings/')
//     console.log("💡 응답 데이터:", res.data)
//     allProducts.value = res.data.data || []  // 백엔드 응답 구조에 따라 조정
//     filterByType(selectedType.value)   // ✅ 초기 필터 적용
//   } catch (err) {
//     console.error('❌ 상품 데이터를 불러오는 데 실패했습니다.', err)
//   }
// })

// ✅ 상품 필터링 + 정렬
const filterByType = (type) => {
  selectedType.value = type
  const filtered = allProducts.value.filter(p => p.type === type) // ✅ 선언
  products.value = sortByOption(filtered, sortOption.value)
  currentPage.value = 1
}

const sortProducts = () => {
  const filtered = allProducts.value.filter(p => p.type === selectedType.value) // ✅ 선언
  products.value = sortByOption(filtered, sortOption.value)
  currentPage.value = 1
}

// ✅ 정렬 함수
const sortByOption = (list, option) => {
  const toFloat = (val) => {
    if (typeof val === 'string') {
      // "3.8%" 혹은 " 4.0 " 같은 문자열 대비
      val = val.replace(/[^\d.-]/g, '')
    }
    const num = parseFloat(val)
    return isNaN(num) ? -Infinity : num
  }

  if (option === 'interest') {
    return [...list].sort((a, b) => toFloat(b.interest_rate) - toFloat(a.interest_rate))
  } else if (option === 'special') {
    return [...list].sort((a, b) => toFloat(b.special_rate) - toFloat(a.special_rate))
  }

  return list
}


// 페이지 수 계산
const totalPages = computed(() => {
  return Math.ceil(products.value.length / itemsPerPage)
})

// 현재 페이지에 해당하는 상품만 보여주기
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return products.value.slice(start, end)
})

// 페이지 변경
const goToPage = (page) => {
  currentPage.value = page
}


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
      id: 3,
      type: "정기예금",
      name: "우리예금",
      company: "우리은행",
      interest_rate: 3.5,
      special_rate: 3.7,
      term: 6,
      target: "만 19세 이상 개인"
    },
    {
      id: 4,
      type: "정기예금",
      name: "test",
      company: "신한은행",
      interest_rate: 2.0,
      special_rate: 4.0,
      term: 24,
      target: "만 19세 이상 개인"
    },
    {
      id: 5,
      type: "정기예금",
      name: "test",
      company: "하나은행",
      interest_rate: 1.8,
      special_rate: 9.0,
      term: 36,
      target: "만 19세 이상 개인"
    },
    {
      id: 6,
      type: "정기예금",
      name: "국민 튼튼예금",
      company: "국민은행",
      interest_rate: 3.2,
      special_rate: 3.8,
      term: 12,
      target: "만 19세 이상 개인"
    },
    {
      id: 7,
      type: "정기예금",
      name: "우리예금",
      company: "우리은행",
      interest_rate: 3.5,
      special_rate: 3.7,
      term: 6,
      target: "만 19세 이상 개인"
    },
    {
      id: 8,
      type: "정기예금",
      name: "test",
      company: "신한은행",
      interest_rate: 2.0,
      special_rate: 4.0,
      term: 24,
      target: "만 19세 이상 개인"
    },
    {
      id: 9,
      type: "정기예금",
      name: "test",
      company: "하나은행",
      interest_rate: 1.8,
      special_rate: 9.0,
      term: 36,
      target: "만 19세 이상 개인"
    },
    {
      id: 10,
      type: "정기예금",
      name: "국민 튼튼예금",
      company: "국민은행",
      interest_rate: 3.2,
      special_rate: 3.8,
      term: 12,
      target: "만 19세 이상 개인"
    },
    {
      id: 11,
      type: "정기예금",
      name: "우리예금",
      company: "우리은행",
      interest_rate: 3.5,
      special_rate: 3.7,
      term: 6,
      target: "만 19세 이상 개인"
    },
    {
      id: 12,
      type: "정기예금",
      name: "test",
      company: "신한은행",
      interest_rate: 2.0,
      special_rate: 4.0,
      term: 24,
      target: "만 19세 이상 개인"
    },
    {
      id: 13,
      type: "정기예금",
      name: "test",
      company: "하나은행",
      interest_rate: 1.8,
      special_rate: 9.0,
      term: 36,
      target: "만 19세 이상 개인"
    },
    {
      id: 14,
      type: "적금",
      name: "test",
      company: "하나은행",
      interest_rate: 1.8,
      special_rate: 9.0,
      term: 36,
      target: "만 19세 이상 개인"
    },
    {
      id: 15,
      type: "적금",
      name: "test",
      company: "국민은행",
      interest_rate: 3.2,
      special_rate: 3.8,
      term: 12,
      target: "만 19세 이상 개인"
    },
    {
      id: 16,
      type: "적금",
      name: "test",
      company: "우리은행",
      interest_rate: 3.5,
      special_rate: 3.7,
      term: 6,
      target: "만 19세 이상 개인"
    },
    {
      id: 17,
      type: "적금",
      name: "test",
      company: "신한은행",
      interest_rate: 2.0,
      special_rate: 4.0,
      term: 24,
      target: "만 19세 이상 개인"
    },
  ]
  filterByType(selectedType.value)
})
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

/* ✅ 버튼 + 드롭다운 가로 배치 */
.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.btn-group {
  display: flex;
  gap: 1rem;
}

/* 기본 버튼 스타일 */
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

.saving-container {
  display: flex;
  flex-wrap: wrap;
  /* ✅ 줄바꿈 허용 */
  justify-content: center;
  /* ✅ 가운데 정렬 */
  gap: 2rem;
  /* ✅ 카드 사이 간격 */
  padding: 2rem;
  max-width: 1200px;
  /* ✅ 전체 최대 너비 제한 */
  margin: 0 auto;
  /* ✅ 가운데 정렬 */
}

/* SavingCard.vue의 루트 div 또는 카드 스타일 */
.saving-card {
  flex: 1 1 300px;
  /* ✅ 기본 너비 300px, 줄어들고 늘어남 허용 */
  max-width: 300px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
  gap: 0.5rem;
}

.pagination button {
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  background-color: white;
  color: #145c2b;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.pagination button:hover {
  background-color: #f0f0f0;
}

.pagination button.active {
  background-color: #145c2b;
  color: white;
  border-color: #145c2b;
}

.heart-count {
  color: var(--text-secondary);
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>
