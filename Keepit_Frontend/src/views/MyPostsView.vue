<template>
  <div class="myposts-container">
    <h1 class="page-title">내가 쓴 글</h1>
    
    <div class="posts-summary">
      <div class="summary-item">
        <span class="summary-label">전체 게시글</span>
        <span class="summary-value">{{ postsCount.total }}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">자유게시판</span>
        <span class="summary-value">{{ postsCount.free }}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">질문게시판</span>
        <span class="summary-value">{{ postsCount.question }}</span>
      </div>
    </div>

    <div class="posts-container">
      <div v-if="loading" class="loading">
        게시글을 불러오는 중입니다...
      </div>
      
      <template v-else>
        <div v-if="posts.length === 0" class="empty-state">
          <i class="fas fa-pen"></i>
          <p>아직 작성한 게시글이 없습니다.</p>
          <div class="action-buttons">
            <router-link :to="{ name: 'freepostcreate' }" class="write-button">
              자유게시판 글쓰기
            </router-link>
            <router-link :to="{ name: 'questioncreate' }" class="write-button">
              질문게시판 글쓰기
            </router-link>
          </div>
        </div>

        <div v-else class="posts-list">
          <div v-for="post in posts" :key="post.id" class="post-item" 
               @click="goToPost(post.board_type, post.id)">
            <div class="post-header">
              <span class="board-type" :class="post.board_type">
                {{ post.board_type === 'free' ? '자유게시판' : '질문게시판' }}
              </span>
              <span v-if="post.board_type === 'question' && post.is_solved" 
                    class="solved-badge">해결</span>
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/users'
import axios from 'axios'

const router = useRouter()
const accountStore = useAccountStore()

const loading = ref(true)
const posts = ref([])
const postsCount = ref({
  total: 0,
  free: 0,
  question: 0
})

onMounted(async () => {
  const token = accountStore.token
  if (!token) {
    alert('⚠️ 로그인이 필요한 서비스입니다.')
    router.push({ name: 'login' })
    return
  }

  try {
    const response = await axios.get('/api/v1/community/my-posts/', {
      headers: {
        Authorization: `Token ${token}`
      }
    })

    if (!response.data) {
      throw new Error('데이터가 없습니다.')
    }

    posts.value = response.data.posts || []
    postsCount.value = {
      total: response.data.total_posts || 0,
      free: response.data.posts_count?.free || 0,
      question: response.data.posts_count?.question || 0
    }
  } catch (error) {
    console.error('게시글 로딩 실패:', error)
    if (error.response) {
      // 서버에서 응답이 왔지만 에러인 경우
      if (error.response.status === 401) {
        alert('로그인이 필요한 서비스입니다.')
        router.push({ name: 'login' })
      } else if (error.response.status === 404) {
        alert('요청한 페이지를 찾을 수 없습니다.')
      } else {
        alert(`서버 오류가 발생했습니다. (${error.response.status})`)
      }
    } else if (error.request) {
      // 요청은 보냈지만 응답이 없는 경우
      alert('서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.')
    } else {
      // 요청 자체를 보내지 못한 경우
      alert('요청을 보내는 중 오류가 발생했습니다.')
    }
  } finally {
    loading.value = false
  }
})

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
}

const goToPost = (type, postId) => {
  const routeName = type === 'free' ? 'freepostdetail' : 'questiondetail'
  router.push({ name: routeName, params: { id: postId } })
}
</script>

<style scoped>
.myposts-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.page-title {
  color: #333;
  margin-bottom: 2rem;
  text-align: center;
}

.posts-summary {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.summary-item {
  text-align: center;
}

.summary-label {
  display: block;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.summary-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #145c2b;
}

.posts-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #666;
}

.empty-state i {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #145c2b;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.write-button {
  padding: 0.8rem 1.5rem;
  border-radius: 6px;
  background: #145c2b;
  color: white;
  text-decoration: none;
  transition: all 0.2s;
}

.write-button:hover {
  background: #0d4420;
  transform: translateY(-2px);
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.post-item {
  padding: 1.5rem;
  border: 1px solid #eee;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.post-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.post-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.board-type {
  font-size: 0.8rem;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  background: #e9ecef;
  color: #495057;
}

.board-type.free {
  background: #e3f2fd;
  color: #1976d2;
}

.board-type.question {
  background: #fbe9e7;
  color: #d84315;
}

.solved-badge {
  font-size: 0.8rem;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  background: #e8f5e9;
  color: #2e7d32;
}

.post-title {
  font-size: 1.1rem;
  color: #333;
  margin: 0.5rem 0;
  font-weight: 500;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #666;
}

.post-date {
  color: #888;
}

.post-stats {
  display: flex;
  gap: 1rem;
}

.likes i {
  color: #e91e63;
}

.comments i {
  color: #2196f3;
}

@media (max-width: 768px) {
  .posts-summary {
    flex-direction: column;
    gap: 1rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .write-button {
    width: 100%;
  }
}
</style> 