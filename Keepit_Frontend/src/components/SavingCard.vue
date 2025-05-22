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

    <div class="icon-box">
      <button class="icon-button search" @click="goToBankPage">
        <i class="fas fa-search"></i>
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
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import bankLinks from '@/assets/data/bankLinks.json'
import { useAccountStore } from '@/stores/users.js'

const accountStore = useAccountStore()
const { token, userId, isAuthenticated } = accountStore

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const getBankImage = (companyName) => {
  return `/images/images_bank/${companyName}.png`
}

const goToBankPage = () => {
  const url =
    bankLinks[props.product.company] ||
    `https://search.naver.com/search.naver?query=${encodeURIComponent(props.product.company)}`
  window.open(url, '_blank')
}

const isFavorite = ref(false)
const isHovered = ref(false)

const toggleFavorite = async () => {

  const url = `/api/v1/products/${props.product.id}/like/`
  const headers = { 'Authorization': `Token ${token}` }

  if (!isFavorite.value) {
    await fetch(url, {
      method: 'POST',
      headers: {
        ...headers,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_id: userId })
    })
    isFavorite.value = true
  } else {
    await fetch(url, { method: 'DELETE', headers })
    isFavorite.value = false
  }
}
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
}

.rate {
  margin: 0.4rem 0;
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
}

.icon-box {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.icon-button {
  border: 2px solid;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  transition: all 0.2s;
  cursor: pointer;
}

.icon-button.search {
  border-color: #145c2b;
  color: #145c2b;
}
.icon-button.search:hover,
.icon-button.search:focus {
  background-color: #145c2b;
  color: white;
}

.icon-button.heart {
  border-color: #e272c0;
  background-color: white;
  color: #e272c0;
}

/* 찜 된 상태 */
.icon-button.heart.active {
  background-color: #e272c0;
  color: white;
}

/* 마우스 호버 중 (찜 안 되어있고, 마우스 올라감) */
.icon-button.heart.hovered {
  background-color: #e272c0;
  color: white;
}
</style>
