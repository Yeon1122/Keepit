<template>
  <div class="my-posts-container">
    <div class="content-card">
      <div class="card-header">
        <h3>{{ pageTitle }}</h3>
      </div>
      <template v-if="loading">
        <div class="loading-state">
          <i class="fas fa-spinner fa-spin"></i>
          <p>게시글을 불러오는 중...</p>
        </div>
      </template>
      <template v-else>
        <div class="posts-summary">
          <div class="summary-item">
            <span class="label">전체</span>
            <span class="value">{{ postsCount.total }}</span>
          </div>
          <div class="summary-item">
            <span class="label">자유게시판</span>
            <span class="value">{{ postsCount.free }}</span>
          </div>
          <div class="summary-item">
            <span class="label">질문게시판</span>
            <span class="value">{{ postsCount.question }}</span>
          </div>
        </div>
        <div v-if="posts.length === 0" class="empty-state">
          <i class="fas fa-file-alt"></i>
          <p>{{ isCurrentUser ? '아직 작성한 글이 없습니다.' : `${authorInfo.nickname}님이 작성한 글이 없습니다.` }}</p>
        </div>
        <div v-else class="posts-list">
          <div v-for="post in posts" :key="post.id" class="post-item" @click="goToPost(post.board_type, post.id)">
            <div class="post-header">
              <span class="board-type" :class="post.board_type">
                {{ post.board_type === 'free' ? '자유게시판' : '질문게시판' }}
              </span>
              <span v-if="post.board_type === 'question' && post.is_solved" class="solved-badge">해결</span>
            </div>
            <div class="post-title">{{ post.title }}</div>
            <div class="post-meta">
              <span class="post-date">{{ formatDate(post.created_at) }}</span>
              <div class="post-stats">
                <span class="likes">
                  <i class="fas fa-heart"></i> {{ post.likes_count }}
                </span>
                <span class="comments">
                  <i class="fas fa-comment"></i> {{ post.comments.length }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAccountStore } from '@/stores/users'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const accountStore = useAccountStore()

const loading = ref(true)
const posts = ref([])
const postsCount = ref({
  total: 0,
  free: 0,
  question: 0
})

const authorInfo = ref({
  userid: '',
  nickname: ''
})

const isCurrentUser = computed(() => {
  return route.query.userid === accountStore.userId
})

const pageTitle = computed(() => {
  if (isCurrentUser.value) {
    return '내가 작성한 글'
  }
  return `${authorInfo.value.nickname}님의 게시글`
})

onMounted(async () => {
  const token = accountStore.token
  if (!token) {
    alert('⚠️ 로그인이 필요한 서비스입니다.')
    router.push({ name: 'login' })
    return
  }

  try {
    const userid = route.query.userid
    const endpoint = userid ? `/api/v1/community/user-posts/${userid}/` : '/api/v1/community/my-posts/'

    const response = await axios.get(endpoint, {
      headers: {
        Authorization: `Token ${token}`
      }
    })

    if (!response.data) {
      throw new Error('데이터가 없습니다.')
    }

    posts.value = response.data.posts
    postsCount.value = {
      total: response.data.total_posts,
      ...response.data.posts_count
    }

    if (response.data.author) {
      authorInfo.value = response.data.author
    }

    loading.value = false
  } catch (err) {
    console.error('게시글 조회 실패:', err)
    alert('게시글을 불러오는데 실패했습니다.')
    loading.value = false
  }
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const goToPost = (boardType, postId) => {
  router.push({
    name: boardType === 'free' ? 'freepostdetail' : 'questionpostdetail',
    params: { postId }
  })
}
</script>

<style scoped>
.my-posts-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
  font-family: 'Pretendard', sans-serif;
}

.content-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.card-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #333;
}

.posts-summary {
  display: flex;
  justify-content: center;
  gap: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.summary-item {
  text-align: center;
}

.summary-item .label {
  display: block;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.summary-item .value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #145c2b;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #666;
}

.loading-state i,
.empty-state i {
  font-size: 2rem;
  color: #145c2b;
  margin-bottom: 1rem;
}

.loading-state p,
.empty-state p {
  margin: 0;
  font-size: 1.1rem;
}

.posts-list {
  padding: 1.5rem;
}

.post-item {
  padding: 1.2rem;
  border-radius: 8px;
  background: #f8f9fa;
  margin-bottom: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.post-item:hover {
  background: #f1f9f3;
  transform: translateX(4px);
}

.post-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 0.8rem;
}

.board-type {
  font-size: 0.85rem;
  padding: 0.3rem 0.8rem;
  border-radius: 999px;
  font-weight: 600;
}

.board-type.free {
  background: #e7f5ec;
  color: #145c2b;
}

.board-type.question {
  background: #fff3cd;
  color: #856404;
}

.solved-badge {
  font-size: 0.85rem;
  padding: 0.3rem 0.8rem;
  border-radius: 999px;
  background: #d4edda;
  color: #155724;
  font-weight: 600;
}

.post-title {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 0.8rem;
  font-weight: 500;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: #666;
}

.post-stats {
  display: flex;
  gap: 1rem;
}

.post-stats span {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.post-stats i {
  font-size: 0.9rem;
}

.likes i {
  color: #dc3545;
}

.comments i {
  color: #145c2b;
}

@media (max-width: 768px) {
  .posts-summary {
    flex-direction: column;
    gap: 1rem;
  }

  .summary-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 1rem;
    background: white;
    border-radius: 8px;
  }

  .summary-item .label {
    margin: 0;
  }

  .summary-item .value {
    font-size: 1.2rem;
  }
}
</style>