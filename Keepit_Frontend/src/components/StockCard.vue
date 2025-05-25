<template>
  <div class="stock-card" @click="handleClick">
    <div class="left" @click.stop>
      <HeartButton
        v-if="showHeart"
        :initial-is-hearted="isLiked"
        @update:hearted="toggleLike"
      />
      <div class="name">{{ props.data.name }}</div>
    </div>
    <div class="price-block">
      <div class="current-price">{{ formatNumber(props.data.current_price) }}원</div>
      <div class="price-change" :class="{ 'up': props.data.price_change > 0, 'down': props.data.price_change < 0 }">
        {{ formatNumber(Math.abs(props.data.price_change)) }}원
        ({{ props.data.price_change > 0 ? '▲' : props.data.price_change < 0 ? '▼' : '-' }})
      </div>
    </div>
    <div class="volume-block">
      <div>{{ formatNumber(props.data.trade_volume) }}주</div>
      <div>{{ formatCompact(props.data.trade_value) }}</div>
    </div>
    <div class="marketcap-block">
      {{ formatMarketCap(props.data.market_cap) }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/users'
import { useRouter } from 'vue-router'
import HeartButton from '@/components/HeartButton.vue'
import axios from 'axios'

const router = useRouter()
const accountStore = useAccountStore()
const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  showHeart: {
    type: Boolean,
    default: false
  }
})

const isLiked = ref(false)
const isHovered = ref(false)

// 초기 찜하기 상태 확인
const checkInitialLikeStatus = async () => {
  const token = accountStore.token
  console.log('초기 상태 확인 시 토큰:', token)
  
  if (!token) return
  
  try {
    const response = await axios({
      method: 'GET',
      url: `http://127.0.0.1:8000/api/v1/products/stocks/${props.data.stock_code}/favorite/`,
      headers: {
        Authorization: `Token ${token}`
      }
    })
    console.log('초기 상태 응답:', response.data)
    isLiked.value = response.data.is_hearted
  } catch (err) {
    console.error('찜하기 상태 확인 오류:', err)
  }
}

// 컴포넌트 마운트 시 찜하기 상태 확인
onMounted(checkInitialLikeStatus)

const toggleLike = async () => {
  try {
    const token = accountStore.token
    console.log('토글 시 토큰:', token)
    
    if (!token) {
      alert('로그인이 필요한 서비스입니다.')
      return
    }

    const method = isLiked.value ? 'DELETE' : 'POST'
    console.log('현재 상태:', isLiked.value, '요청 메서드:', method)

    const response = await axios({
      method,
      url: `http://127.0.0.1:8000/api/v1/products/stocks/${props.data.stock_code}/favorite/`,
      headers: {
        Authorization: `Token ${token}`
      }
    })
    console.log('API 응답:', response.data)
    
    // 상태 업데이트
    if (method === 'POST') {
      isLiked.value = true
    } else {
      isLiked.value = false
    }
  } catch (err) {
    console.error('찜하기 오류:', err)
    if (err.response?.status === 401) {
      alert('로그인이 필요한 서비스입니다.')
    } else {
      alert('찜하기 처리에 실패했습니다.')
    }
  }
}

const handleClick = () => {
  router.push({
    name: 'stockdetail',
    params: { stock_code: props.data.stock_code }
  })
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
  cursor: pointer;
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
  color: #333;
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
  color: #333;
}

.price-change {
  color: #333;
}

.up {
  color: #e64545;
}

.down {
  color: #14449c;
}
</style>
