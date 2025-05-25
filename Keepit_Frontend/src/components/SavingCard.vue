<!-- 초기 찜 상태 확인 백엔드와 조율 필요 -->

<template>
  <div class="card">
    <div class="card-header">
      <p class="company">{{ props.product.company }}</p>
      <img
        class="bank-logo"
        :src="getBankImage(props.product.company)"
        :alt="props.product.company"
      />
    </div>

    <h3 class="product-name">{{ props.product.name }}</h3>

    <p class="rate">
      <span class="base">{{ props.product.interest_rate }}%</span>
      <span> ~ </span>
      <span class="special">{{ props.product.special_rate }}%</span>
    </p>

    <p class="term">가입기간: {{ props.product.term || '정보 없음' }}개월</p>
    <p class="target">가입대상: {{ props.product.target || '해당 없음' }}</p>

    <div class="button-container">
      <button class="icon-button search" @click.stop="goToBank">
        <i class="fas fa-search"></i>
        <span class="tooltip">더보기</span>
      </button>
      <button
        v-if="isAuthenticated"
        class="icon-button heart"
        :class="{
          active: isFavorite,
          hovered: !isFavorite && isHovered
        }"
        @mouseenter="isHovered = true"
        @mouseleave="isHovered = false"
        @click.prevent.stop="toggleFavorite"
      >
        <i :class="[isFavorite ? 'fas' : 'far', 'fa-heart']"></i>
        <span class="tooltip">찜하기</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import bankLinks from '@/assets/data/bankLinks.json'
import { useAccountStore } from '@/stores/users.js'
import { useMessageStore } from '@/stores/message'
import axios from 'axios'

const accountStore = useAccountStore()
const messageStore = useMessageStore()
const isAuthenticated = computed(() => accountStore.isAuthenticated)

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const getBankImage = (companyName) => {
  return `/images/images_bank/${companyName}.png`
}

const goToBank = () => {
  const bankUrl = bankLinks[props.product.company]
  if (bankUrl) {
    window.open(bankUrl, '_blank')
  } else {
    // 은행 링크가 없는 경우 네이버 검색
    const searchQuery = encodeURIComponent(`${props.product.company} ${props.product.name}`)
    window.open(`https://search.naver.com/search.naver?query=${searchQuery}`, '_blank')
  }
}

const isFavorite = ref(props.product.is_liked || false)
const isHovered = ref(false)

const toggleFavorite = async (e) => {
  console.log('찜하기 버튼 클릭됨')
  e.stopPropagation()  // 이벤트 전파 중단
  
  if (!isAuthenticated.value) {
    alert('로그인이 필요한 서비스입니다.')
    return
  }

  const productId = props.product.id
  console.log('상품 ID:', productId)
  const headers = { Authorization: `Token ${accountStore.token}` }

  try {
    let response
    if (!isFavorite.value) {
      console.log('찜하기 추가 시도')
      // 찜하기 추가
      response = await axios.post(`http://127.0.0.1:8000/api/v1/products/favorites/by-id/${productId}/`, {}, { headers })
      console.log('찜하기 추가 응답:', response.data)
      isFavorite.value = true
    } else {
      console.log('찜하기 삭제 시도')
      // 찜하기 삭제
      response = await axios.delete(`http://127.0.0.1:8000/api/v1/products/favorites/by-id/${productId}/`, { headers })
      console.log('찜하기 삭제 응답:', response.data)
      isFavorite.value = false
    }
  } catch (err) {
    console.error('찜하기 처리 실패:', err.response || err)
    alert('찜하기 처리에 실패했습니다.')
  }
}

const checkFavoriteStatus = async () => {
  if (!accountStore.isAuthenticated) {
    isFavorite.value = false
    return
  }

  const productId = props.product.id
  const headers = { Authorization: `Token ${accountStore.token}` }

  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/products/favorites/by-id/${productId}/`, { headers })
    isFavorite.value = response.data.is_liked || false
  } catch (err) {
    console.error('찜하기 상태 확인 실패:', err)
    isFavorite.value = false
  }
}

onMounted(() => {
  if (isAuthenticated.value) {
    checkFavoriteStatus()
  }
})
</script>

<style scoped>
.card {
  border: 2px solid #dcdcdc;
  border-radius: 8px;
  padding: 1rem;
  background-color: white;
  width: 100%;
  max-width: 280px;
  position: relative;
  font-family: 'Pretendard', sans-serif;
  transition: border 0.2s;
  min-height: 250px; /* 최소 높이 설정 */
  display: flex;
  flex-direction: column;
}

.card:hover {
  border: 2px solid #145c2b;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.company {
  font-size: 0.8rem;
  color: #888;
  margin: 0;
}

.bank-logo {
  width: 36px;
  height: 36px;
  object-fit: contain;
}

.product-name {
  font-size: 1.1rem;
  font-weight: bold;
  margin: 0.5rem 0;
  color: #333;
}

.rate {
  margin: 0.4rem 0;
  color: #333;
}

.base {
  color: #999;
  font-weight: 500;
}

.special {
  color: #e64545;
  font-weight: bold;
}

.term,
.target {
  font-size: 0.85rem;
  margin: 0.25rem 0;
  color: #333;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: auto;
  padding-top: 1rem;
}

.icon-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.3s ease;
}

.icon-button:hover {
  background-color: #f5f5f5;
}

.icon-button.search {
  color: #145c2b;
}

.icon-button.heart {
  color: #e64545;
}

.icon-button.heart.active {
  color: #e64545;
  animation: heartBeat 0.3s ease-in-out;
}

.icon-button.heart.hovered {
  color: #ff6b6b;
}

.icon-button .tooltip {
  position: absolute;
  bottom: -30px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.icon-button:hover .tooltip {
  opacity: 1;
  visibility: visible;
  bottom: -25px;
}

@keyframes heartBeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}
</style>
