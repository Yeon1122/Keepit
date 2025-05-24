<template>
  <div class="goods-view">
    <h3>현물 상품 안내</h3>

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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import HeartButton from '@/components/HeartButton.vue'

const allData = ref([])
const goods = ref([])
const likedItems = ref([])
const hoveredItem = ref(null)

const toggleFavorite = (id) => {
  if (likedItems.value.includes(id)) {
    likedItems.value = likedItems.value.filter((itemId) => itemId !== id)
  } else {
    likedItems.value.push(id)
  }
}

const formatPrice = (price) => price.toLocaleString()

onMounted(() => {
  // 🔧 API 연결용
  // const res = await axios.get('http://localhost:8000/api/v1/products/goods/')
  // allData.value = res.data
  // goods.value = allData.value.filter(item => item.type === '현물')

  // 🔧 더미 데이터
  allData.value = [
    { id: 1, type: '현물', name: '금', current_price: 74000 },
    { id: 2, type: '현물', name: '은', current_price: 910 },
    { id: 3, type: '현물', name: '원유', current_price: 84000 },
  ]
  goods.value = allData.value.filter(item => item.type === '현물')
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
</style>
