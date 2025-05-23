<template>
  <div class="news-card">
    <a :href="news.url" target="_blank" rel="noopener noreferrer">
      <h4 class="news-title">{{ news.title }}</h4>
      <p class="news-date">{{ formatDate(news.date) }}</p>
    </a>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  news: {
    type: Object,
    required: true
  }
})

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}
</script>

<style scoped>
.news-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 0.8rem 1rem;
  margin-bottom: 0.7rem;
  background-color: #fafafa;
  transition: background-color 0.2s;
}

.news-card:hover {
  background-color: #f1f1f1;
}

.news-title {
  margin: 0;
  font-size: 0.95rem;
  font-weight: bold;
  color: #145c2b;
}

.news-date {
  margin: 0.2rem 0 0;
  font-size: 0.8rem;
  color: #666;
}
</style>
