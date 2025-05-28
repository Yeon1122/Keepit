<template>
  <div class="goods-view">
    <h3>현물 상품 안내</h3>

    <!-- 로딩 상태 -->
    <div v-if="loading" class="loading-overlay">
      <lottie-player
        :animationData="loadingAnimation"
        :loop="true"
        :autoplay="true"
        style="width: 200px; height: 200px;"
      />
      <p class="loading-text">현물 데이터를 불러오는 중입니다...</p>
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
        <div class="name-col header-text">종목</div>
        <div class="price-col header-text">현재가</div>
        <div class="change-col header-text">변동가</div>
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
        <div class="price-col">
          ${{ formatPrice(item.current_price) }} / oz
        </div>
        <div class="change-col" :class="getPriceChangeClass(item.price_change)">
          <i :class="['fas', item.price_change > 0 ? 'fa-caret-up' : 'fa-caret-down']"></i>
          {{ formatPriceChange(item.price_change) }}
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import HeartButton from '@/components/HeartButton.vue'
import { useAccountStore } from '@/stores/users'
import axios from 'axios'
import loadingAnimation from '@/assets/animations/gold_loading.json'
import LottiePlayer from '@/components/LottiePlayer.vue'

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
      url: `/api/v1/products/goods/${id}/favorite/`,
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

const formatPriceChange = (change) => {
  if (!change) return '0'
  return Math.abs(change).toLocaleString()
}

const getPriceChangeClass = (change) => {
  if (change > 0) {
    return 'positive-change'
  } else if (change < 0) {
    return 'negative-change'
  } else {
    return ''
  }
}

const fetchData = async () => {
  loading.value = true
  error.value = null

  try {
    // 현물 상품 데이터 가져오기
    const goodsRes = await axios.get('/api/v1/products/goods/')
    goods.value = goodsRes.data
    console.log('현물 데이터:', goods.value)

    // 찜한 상품 목록 가져오기
    if (isAuthenticated.value) {
      // 각 현물 상품의 찜하기 상태를 개별적으로 확인
      const likedIds = []
      for (const item of goods.value) {
        try {
          const favRes = await axios.get(`/api/v1/products/goods/${item.id}/favorite/`, {
            headers: { Authorization: `Token ${accountStore.token}` }
          })
          if (favRes.data.is_liked) {
            likedIds.push(item.id)
          }
        } catch (err) {
          console.log(`상품 ${item.id} 찜하기 상태 확인 실패:`, err)
        }
      }
      likedItems.value = likedIds
      console.log('현물 찜한 상품 ID들:', likedItems.value)
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

.header-text {
  color: white !important;
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
  color: #333;
  min-width: 120px;
  white-space: nowrap;
}

/* 변동가 영역 */
.change-col {
  flex: 2;
  text-align: center;
  font-weight: bold;
  min-width: 100px;
  white-space: nowrap;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.3rem;
}

.change-col i {
  font-size: 1.2rem;
}

.positive-change {
  color: #dc3545;
}

.negative-change {
  color: #007bff;
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

.error-state {
  text-align: center;
  padding: 2rem;
  color: #666;
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
