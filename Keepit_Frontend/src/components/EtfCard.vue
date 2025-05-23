<template>
  <div class="etf-card">
    <div class="left">
      <button class="heart-button"
              :class="{ active: isLiked, hovered: !isLiked && isHovered }"
              @mouseenter="isHovered = true"
              @mouseleave="isHovered = false"
              @click.stop="toggleFavorite">
        <i :class="[isLiked ? 'fas' : 'far', 'fa-heart']"></i>
      </button>
      <div class="etf-info">
        <div class="name">{{ data.name }}</div>
        <div class="sector">{{ data.sector }}</div>
      </div>
    </div>

    <div class="price-block">
      <div class="current-price"
           :class="{
             red: data.price_change > 0,
             blue: data.price_change < 0,
             black: data.price_change === 0
           }">
        {{ formatNumber(data.current_price) }}원
      </div>
      <div class="price-change"
           :class="{
             red: data.price_change > 0,
             blue: data.price_change < 0,
             black: data.price_change === 0
           }">
        전일 대비 {{ formatChange(data.price_change) }}
      </div>
    </div>

    <div class="nav-block">
      <div class="nav"
           :class="{
             red: data.nav_change > 0,
             blue: data.nav_change < 0,
             black: data.nav_change === 0
           }">
        {{ formatNumber(data.nav) }}원
      </div>
      <div class="price-change"
           :class="{
             red: data.nav_change > 0,
             blue: data.nav_change < 0,
             black: data.nav_change === 0
           }">
        전일 대비 {{ formatChange(data.nav_change) }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/users.js'
import axios from 'axios'

const props = defineProps({
  data: Object
})

const accountStore = useAccountStore()
const token = accountStore.token

const isLiked = ref(false)
const isHovered = ref(false)

const toggleFavorite = async () => {
  if (!token) {
    alert('로그인이 필요합니다.')
    return
  }

  try {
    const url = `http://127.0.0.1:8000/api/v1/products/${props.data.id}/favorite/`
    const headers = {
      Authorization: `Token ${token}`
    }

    if (isLiked.value) {
      await axios.delete(url, { headers })
    } else {
      await axios.post(url, {}, { headers })
    }

    isLiked.value = !isLiked.value
  } catch (error) {
    console.error('찜하기 오류:', error)
  }
}

const formatNumber = (val) => {
  return val == null ? '-' : Number(val).toLocaleString()
}

const formatChange = (val) => {
  if (val > 0) return `+${val.toLocaleString()}`
  if (val < 0) return `${val.toLocaleString()}`
  return '0'
}
</script>

<style scoped>
.etf-card {
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

.etf-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.left {
  flex: 2;
  display: flex;
  align-items: center;
  gap: 0.7rem;
}

.etf-info {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.name {
  font-weight: 600;
  font-size: 1.1rem;
}

.sector {
  font-size: 0.85rem;
  color: #666;
}

.price-block {
  flex: 1.5;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  text-align: right;
}

.current-price {
  font-weight: bold;
  font-size: 1rem;
}

.price-change {
  font-size: 0.85rem;
  color: #666;
}

.nav-block {
  text-align: right;
  flex: 1.5;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.nav {
  font-weight: bold;
  font-size: 1rem;
}

.heart-button {
  border: 2px solid #e272c0;
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
  color: #e272c0;
}

.heart-button.active,
.heart-button.hovered {
  background-color: #e272c0;
  color: white;
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