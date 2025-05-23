<template>
  <div class="stock-card">
    <div class="left">
      <button class="heart-button"
              :class="{ active: isLiked, hovered: !isLiked && isHovered }"
              @mouseenter="isHovered = true"
              @mouseleave="isHovered = false"
              @click="toggleFavorite">
        <i :class="[isLiked ? 'fas' : 'far', 'fa-heart']"></i>
      </button>
      <div class="info">
        <div class="name">{{ data.name }}</div>
      </div>
    </div>

    <div class="price-block">
      <div
        class="current-price"
        :class="{
          red: data.current_price > data.base_price,
          blue: data.current_price < data.base_price,
          black: data.current_price === data.base_price
        }"
      >
        {{ formatNumber(data.current_price) }}
      </div>
      <div class="base-price">
        Start <span class="base-price-value">{{ formatNumber(data.base_price) }}</span>
      </div>
    </div>

    <div class="volume-block">
      <div class="current-volume">{{ formatNumber(data.trade_volume) }}</div>
      <div class="current-total-value">{{ formatCompact(data.trade_value) }}</div>
    </div>

    <div class="marketcap-block">
      <div class="current-cap">{{ formatMarketCap(data.market_cap) }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/users.js'

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const accountStore = useAccountStore()
const isLiked = ref(false)

const toggleFavorite = async () => {
  if (!accountStore.token) {
    alert('로그인 후 이용해주세요')
    return
  }

  try {
    if (isLiked.value) {
      await axios.delete(`http://127.0.0.1:8000/api/v1/products/${props.data.id}/unfavorite/`)
    } else {
      await axios.post(`http://127.0.0.1:8000/api/v1/products/${props.data.id}/favorite/`)
    }
    isLiked.value = !isLiked.value
  } catch (err) {
    console.error('찜하기 오류:', err)
  }
}

const formatNumber = (val) => {
  if (val === null || val === undefined) return '-'
  return Number(val).toLocaleString()
}

const formatCompact = (val) => {
  if (val >= 100000000) return `${(val / 100000000).toLocaleString()}백만`
  if (val >= 10000) return `${(val / 10000).toLocaleString()}만원`
  return `${val}원`
}

const formatMarketCap = (val) => {
  if (val >= 1e13) {
    return `${Math.floor(val / 1e13)}조 ${Math.floor((val % 1e13) / 1e9)}억`
  } else if (val >= 1e12) {
    return `${(val / 1e12).toFixed(1)}조`
  }
  return `${formatCompact(val)}`
}
</script>

<style scoped>
.stock-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  margin-bottom: 1rem;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 0.95rem;
  transition: box-shadow 0.2s;
}

.stock-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.left {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  flex: 2;
}

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

.name {
  font-weight: 600;
  font-size: 1rem;
}

.price-block{
  display: flex;
  flex-direction: column;
  align-items: right;
  flex: 1.2;
  text-align: right;
}


.volume-block {
  display: flex;
  flex-direction: column;
  align-items: right;
  flex: 1.5;
  text-align: right;
}


.marketcap-block {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  flex: 1.2;
  text-align: right;
}

.current-price {
  font-weight: bold;
  font-size: 1rem;
}

.base-price {
  font-size: 0.8rem;
  color: #888;
}

.base-price-value {
  font-size: 0.8rem;
  color: #888;
}

.current-volume,
.current-total-value,
.current-cap {
  font-weight: bold;
  font-size: 0.9rem;
  color: #555; /* 회색과 검정 중간톤 */
}

.red {
  color: #e64545;
}

.blue {
  color: #14449c;
}

.black {
  color: #000;
}
</style>
