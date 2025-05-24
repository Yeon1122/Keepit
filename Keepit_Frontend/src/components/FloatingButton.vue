<template>
  <div class="floating-container" :class="{ 'is-open': isOpen }">
    <div class="floating-buttons">
      <button class="floating-button sub-button location" @click="handleLocation">
        <i class="fas fa-location-dot"></i>
        <span class="button-label">지점찾기</span>
      </button>
      <button class="floating-button sub-button support" @click="handleSupport">
        <i class="fas fa-robot"></i>
        <span class="button-label">AI 챗봇</span>
      </button>
    </div>
    <button class="floating-button main-button" @click="toggleMenu">
      <i class="fas fa-ellipsis" :class="{ 'rotate': isOpen }"></i>
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isOpen = ref(false)

const toggleMenu = () => {
  isOpen.value = !isOpen.value
}

const handleLocation = () => {
  router.push({ name: 'location' }) // 지점찾기 페이지로 이동
  isOpen.value = false
}

const handleSupport = () => {
  router.push({ name: 'chatbot' }) // AI 챗봇 페이지로 이동
  isOpen.value = false
}
</script>

<style scoped>
.floating-container {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  z-index: 1000;
}

.floating-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.3s ease;
  pointer-events: none;
}

.is-open .floating-buttons {
  opacity: 1;
  transform: translateY(0);
  pointer-events: all;
}

.floating-button {
  border: none;
  border-radius: 50%;
  width: 3.5rem;
  height: 3.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.main-button {
  background-color: #f5f5f5;
  color: #145c2b;
  font-size: 1.5rem;
}

.main-button:hover {
  background-color: #e0e0e0;
  transform: scale(1.05);
}

.main-button i {
  transition: transform 0.3s ease;
}

.main-button i.rotate {
  transform: rotate(270deg);
}

.sub-button {
  background-color: #145c2b;
  color: white;
  font-size: 1.2rem;
}

.sub-button:hover {
  background-color: #0d4420;
  transform: scale(1.05);
}

.button-label {
  position: absolute;
  right: 120%;
  background-color: #333;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.9rem;
  white-space: nowrap;
  opacity: 0;
  transform: translateX(10px);
  transition: all 0.3s ease;
  pointer-events: none;
}

.sub-button:hover .button-label {
  opacity: 1;
  transform: translateX(0);
}

/* 모바일 대응 */
@media (max-width: 768px) {
  .floating-container {
    bottom: 1.5rem;
    right: 1.5rem;
  }

  .floating-button {
    width: 3rem;
    height: 3rem;
  }

  .button-label {
    display: none;
  }
}
</style> 