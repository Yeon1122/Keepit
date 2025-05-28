<template>
  <button 
    class="like-button"
    :class="{ 'liked': isLiked }"
    @click="toggleLike"
    :disabled="isLoading"
  >
    <i class="fas" :class="isLiked ? 'fa-thumbs-up' : 'fa-thumbs-up'"></i>
    <span v-if="showCount" class="like-count">{{ likeCount }}</span>
  </button>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  initialIsLiked: {
    type: Boolean,
    default: false
  },
  initialCount: {
    type: Number,
    default: 0
  },
  showCount: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:liked', 'update:count'])

const isLiked = ref(props.initialIsLiked)
const likeCount = ref(props.initialCount)
const isLoading = ref(false)

const toggleLike = async () => {
  if (isLoading.value) return
  
  isLoading.value = true
  try {
    // 좋아요 상태 토글
    isLiked.value = !isLiked.value
    likeCount.value += isLiked.value ? 1 : -1
    
    // 부모 컴포넌트에 상태 변경 알림
    emit('update:liked', isLiked.value)
    emit('update:count', likeCount.value)
  } catch (error) {
    console.error('Like toggle failed:', error)
    // 실패 시 상태 복구
    isLiked.value = !isLiked.value
    likeCount.value += isLiked.value ? 1 : -1
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.like-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  background: none;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 20px;
}

.like-button:hover {
  background: rgba(20, 92, 43, 0.1);
  color: #145c2b;
}

.like-button.liked {
  color: #145c2b;
}

.like-button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.like-count {
  font-size: 0.9rem;
  font-weight: 500;
}

.fas {
  font-size: 1.2rem;
}
</style> 