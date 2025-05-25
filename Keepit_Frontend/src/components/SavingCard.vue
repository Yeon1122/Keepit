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
      <button class="icon-button search" @click="goToBank">
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
        @click="toggleFavorite"
      >
        <i :class="[isFavorite ? 'fas' : 'far', 'fa-heart']"></i>
        <span class="tooltip">찜하기</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import bankLinks from '@/assets/data/bankLinks.json'
import { useAccountStore } from '@/stores/users.js'
import { useMessageStore } from '@/stores/message'
import axios from 'axios'

const accountStore = useAccountStore()
const messageStore = useMessageStore()
const { token, isAuthenticated } = accountStore

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
  e.stopPropagation() // 이벤트 버블링 방지
  
  try {
    const productId = props.product.id
    const headers = { 
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    }

    let response
    if (!isFavorite.value) {
      // 찜하기 추가
      response = await axios.post(`/api/v1/products/favorites/by-id/${productId}/`, {}, { headers })
      if (response.status === 200 || response.status === 201) {
        isFavorite.value = true
        messageStore.showMessage('찜하기가 완료되었습니다.', 'success')
      }
    } else {
      // 찜하기 취소
      response = await axios.delete(`/api/v1/products/favorites/by-id/${productId}/`, { headers })
      if (response.status === 200 || response.status === 204) {
        isFavorite.value = false
        messageStore.showMessage('찜하기가 해제되었습니다.', 'success')
      }
    }
  } catch (err) {
    console.error('찜하기 오류:', err)
    let errorMessage = '찜하기 처리 중 오류가 발생했습니다.'
    if (err.response) {
      if (err.response.status === 404) {
        errorMessage = '해당 상품을 찾을 수 없습니다.'
      } else if (err.response.status === 401) {
        errorMessage = '로그인이 필요한 서비스입니다.'
      } else if (err.response.status === 400) {
        errorMessage = err.response.data.message || '잘못된 요청입니다.'
      }
    }
    messageStore.showMessage(errorMessage, 'error')
  }
}

const checkFavoriteStatus = async () => {
  if (!isAuthenticated) return

  try {
    const productId = props.product.id
    const headers = { 
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    }

    const response = await axios.get(`/api/v1/products/favorites/by-id/${productId}/`, { headers })
    isFavorite.value = response.data.is_liked || false
  } catch (err) {
    console.error('찜하기 상태 확인 오류:', err)
    // 404나 다른 에러의 경우 찜하지 않은 상태로 간주
    isFavorite.value = false
  }
}

onMounted(() => {
  if (isAuthenticated) {
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
