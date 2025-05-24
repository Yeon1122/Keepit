<template>
  <button 
    class="heart-button"
    :class="{ 'hearted': isHearted }"
    @click="toggleHeart"
    :disabled="isLoading"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <i class="far fa-heart" :class="{ 'fas': isHearted }"></i>
    <span v-if="showCount" class="heart-count">{{ heartCount }}</span>
  </button>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  initialIsHearted: {
    type: Boolean,
    default: false
  },
  initialCount: {
    type: Number,
    default: 0
  },
  showCount: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:hearted', 'update:count'])

const isHearted = ref(props.initialIsHearted)
const heartCount = ref(props.initialCount)
const isLoading = ref(false)
const isHovered = ref(false)

const toggleHeart = async () => {
  if (isLoading.value) return
  
  isLoading.value = true
  try {
    // 찜하기 상태 토글
    isHearted.value = !isHearted.value
    heartCount.value += isHearted.value ? 1 : -1
    
    // 부모 컴포넌트에 상태 변경 알림
    emit('update:hearted', isHearted.value)
    emit('update:count', heartCount.value)
  } catch (error) {
    console.error('Heart toggle failed:', error)
    // 실패 시 상태 복구
    isHearted.value = !isHearted.value
    heartCount.value += isHearted.value ? 1 : -1
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.heart-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: 2px solid #e272c0;
  border-radius: 50%;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0;
  box-sizing: border-box;
}

/* 기본 상태 (찜 안됨) */
.heart-button i {
  color: #e272c0;
  font-size: 1rem;
  transition: all 0.2s ease;
}

/* 찜된 상태 */
.heart-button.hearted i {
  color: #e272c0;
}

/* 호버 상태 */
.heart-button:hover {
  border-color: white;
  background-color: #e272c0;
}

.heart-button:hover i {
  color: white;
}

.heart-button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.heart-count {
  font-size: 0.9rem;
  font-weight: 500;
  margin-left: 0.5rem;
}

/* 하트 애니메이션 */
.heart-button.hearted .fas {
  animation: heartBeat 0.3s ease-in-out;
}

@keyframes heartBeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.3); }
  100% { transform: scale(1); }
}
</style> 