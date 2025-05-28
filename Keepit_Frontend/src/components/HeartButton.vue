<template>
  <button
    class="icon-button heart"
    :class="{
      active: isHearted,
      hovered: !isHearted && isHovered
    }"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
    @click="toggleHeart"
    :disabled="isLoading"
  >
    <i :class="[isHearted ? 'fas' : 'far', 'fa-heart']"></i>
    <span v-if="showCount" class="tooltip">찜하기</span>
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

.icon-button.heart {
  color: #e64545;
}

.icon-button.heart.active {
  color: #e64545;
  animation: heartBeat 0.3s ease-in-out;
}

.tooltip {
  position: absolute;
  bottom: -25px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  white-space: nowrap;
  display: none;
}

.icon-button:hover .tooltip {
  display: block;
}

@keyframes heartBeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.3); }
  100% { transform: scale(1); }
}
</style> 