<template>
  <Transition name="fade">
    <div v-if="messageStore.isVisible" :class="['message-toast', messageStore.type]">
      {{ messageStore.message }}
      <button class="close-button" @click="messageStore.hideMessage">
        <i class="fas fa-times"></i>
      </button>
    </div>
  </Transition>
</template>

<script setup>
import { useMessageStore } from '@/stores/message'

const messageStore = useMessageStore()
</script>

<style scoped>
.message-toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 1rem 2rem;
  border-radius: 8px;
  color: white;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 1rem;
  z-index: 9999;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.success {
  background-color: #10b981;
}

.error {
  background-color: #ef4444;
}

.info {
  background-color: #3b82f6;
}

.warning {
  background-color: #f59e0b;
}

.close-button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 4px;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.close-button:hover {
  opacity: 1;
}

/* 트랜지션 애니메이션 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style> 