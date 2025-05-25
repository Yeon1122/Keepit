<template>
  <div class="goods-view">
    <h3>현물 상품 안내</h3>

    <!-- 로딩 상태 -->
    <div v-if="loading" class="loading-state">
      데이터를 불러오는 중입니다...
    </div>

    <!-- 에러 상태 -->
    <div v-else-if="error" class="error-state">
      {{ error }}
      <button @click="fetchData" class="retry-button">다시 시도</button>
    </div>

    <!-- 데이터 표시 -->
    <template v-else>
      <!-- 헤더 -->
      <div class="header-row">
        <div class="left-col"></div>
        <div class="name-col" style="color: white;">종목</div>
        <div class="price-col" style="color: white;">현재가</div>
      </div>

      <div v-if="goods.length === 0" class="no-data">표시할 현물 상품이 없습니다.</div>

      <div v-for="item in goods" :key="item.id" class="data-row">
        <!-- ❤️ 찜 버튼 -->
        <div class="left-col">
          <HeartButton
            v-if="isAuthenticated"
            :initial-is-hearted="likedItems.includes(item.id)"
            @update:hearted="(value) => handleLike(item.id, value)"
          />
        </div>
        <div class="name-col">{{ item.name }}</div>
        <div class="price-col">{{ formatPrice(item.current_price) }}원</div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import HeartButton from '@/components/HeartButton.vue'
import { useAccountStore } from '@/stores/users'
import axios from 'axios'

const accountStore = useAccountStore()
const isAuthenticated = computed(() => accountStore.isAuthenticated)

const allData = ref([])
const goods = ref([])
const likedItems = ref([])
const loading = ref(true)
const error = ref(null)

const handleLike = async (id, value) => {
  if (!isAuthenticated.value) {
    alert('로그인이 필요한 서비스입니다.')
    return
  }

  try {
    const method = value ? 'POST' : 'DELETE'
    await axios({
      method,
      url: `http://127.0.0.1:8000/api/v1/products/goods/${id}/favorite/`,
      headers: { Authorization: `Token ${accountStore.token}` }
    })

    if (value) {
      likedItems.value.push(id)
    } else {
      likedItems.value = likedItems.value.filter(itemId => itemId !== id)
    }
  } catch (err) {
    console.error('찜하기 실패:', err)
    alert('찜하기 처리에 실패했습니다.')
  }
}

const formatPrice = (price) => price?.toLocaleString() || '-'

const fetchData = async () => {
  loading.value = true
  error.value = null

  try {
    // 현물 상품 데이터 가져오기
    const goodsRes = await axios.get('http://127.0.0.1:8000/api/v1/products/goods/')
    goods.value = goodsRes.data

    // 찜한 상품 목록 가져오기
    if (isAuthenticated.value) {
      const favRes = await axios.get('http://127.0.0.1:8000/api/v1/users/favorites/', {
        headers: { Authorization: `Token ${accountStore.token}` }
      })
      likedItems.value = favRes.data
        .filter(item => item.type === 'goods')
        .map(item => item.id)
    }
  } catch (err) {
    console.error('데이터 로딩 실패:', err)
    error.value = '데이터를 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.goods-view {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

h3 {
  color: #145c2b;
  font-weight: bold;
  font-size: 1.3rem;
  margin-bottom: 1rem;
}

.header-row {
  display: flex;
  align-items: center;
  background-color: #145c2b;
  color: white;
  font-weight: bold;
  padding: 0.8rem 1rem;
  border-radius: 12px;
  margin-bottom: 1rem;
}


/* 동일한 구조 유지 */
.data-row {
  display: flex;
  align-items: center;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 0.8rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

/* ❤️ 찜 버튼 영역 */
.left-col {
  width: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 종목 영역 */
.name-col {
  flex: 2;
  text-align: center;
  font-weight: 500;
  color: #333;
}

/* 가격 영역 */
.price-col {
  flex: 2;
  text-align: center;
  font-weight: bold;
  color: #145c2b;
  min-width: 80px;
  white-space: nowrap;
}

.no-data {
  padding: 1rem;
  color: #888;
  text-align: center;
}

/* ❤️ 찜 버튼 스타일 */
.heart-button {
  border: 2px solid #e272c0;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  transition: all 0.2s;
  cursor: pointer;
  color: #e272c0;
}

.heart-button.active,
.heart-button.hovered {
  background-color: #e272c0;
  color: white;
}

.item-image {
  position: relative;
  width: 100%;
  padding-bottom: 100%;
  overflow: hidden;
}

.item-image img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.heart-button {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1;
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
</style>
