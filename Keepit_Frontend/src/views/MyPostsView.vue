<template>
  <div class="my-posts-container">
    <h2 class="page-title">내가 쓴 글</h2>

    <!-- 자유 게시판 섹션 -->
    <div class="board-section">
      <h3>자유 게시판</h3>
      <div class="posts-list">
        <template v-if="freePosts.length">
          <div v-for="post in freePosts" :key="post.id" class="post-item" @click="goToPost('free', post.id)">
            <div class="post-main">
              <div class="post-title">{{ post.title }}</div>
              <div class="post-content">{{ post.content }}</div>
            </div>
            <div class="post-info">
              <span class="post-date">{{ formatDate(post.created_at) }}</span>
              <div class="post-stats">
                <span class="likes"><i class="fa-solid fa-heart"></i> {{ post.likes }}</span>
                <span class="comments"><i class="fa-solid fa-comment"></i> {{ post.comments?.length || 0 }}</span>
              </div>
              <LikeButton
                :initial-is-liked="post.is_liked"
                :initial-count="post.likes"
                :show-count="true"
                @click.stop
              />
            </div>
          </div>
        </template>
        <div v-else class="no-posts">
          자유 게시판에 작성한 글이 없습니다.
        </div>
      </div>
    </div>

    <!-- 질문 게시판 섹션 -->
    <div class="board-section">
      <h3>질문 게시판</h3>
      <div class="posts-list">
        <template v-if="questionPosts.length">
          <div v-for="post in questionPosts" :key="post.id" class="post-item" @click="goToPost('question', post.id)">
            <div class="post-main">
              <div class="post-title">
                {{ post.title }}
                <span class="solved-badge" v-if="post.is_solved">해결됨</span>
              </div>
              <div class="post-content">{{ post.content }}</div>
            </div>
            <div class="post-info">
              <span class="post-date">{{ formatDate(post.created_at) }}</span>
              <div class="post-stats">
                <span class="likes"><i class="fa-solid fa-heart"></i> {{ post.likes }}</span>
                <span class="comments"><i class="fa-solid fa-comment"></i> {{ post.comments?.length || 0 }}</span>
              </div>
              <LikeButton
                :initial-is-liked="post.is_liked"
                :initial-count="post.likes"
                :show-count="true"
                @click.stop
              />
            </div>
          </div>
        </template>
        <div v-else class="no-posts">
          질문 게시판에 작성한 글이 없습니다.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import LikeButton from '@/components/LikeButton.vue'

const router = useRouter()
const freePosts = ref([])
const questionPosts = ref([])

onMounted(async () => {
  const raw = localStorage.getItem('account')
  const parsed = raw ? JSON.parse(raw) : null
  const localToken = parsed?.token

  if (!localToken) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
    return
  }

  try {
    const res = await axios.get('http://localhost:8000/api/v1/community/my-posts/', {
      headers: {
        Authorization: `Token ${localToken}`
      }
    })
    
    // 게시글 분류
    if (Array.isArray(res.data)) {
      freePosts.value = res.data.filter(post => post.type === 'free' || post.board_type === 'free')
      questionPosts.value = res.data.filter(post => post.type === 'question' || post.board_type === 'question')
    } else {
      console.error('API 응답이 배열 형태가 아닙니다:', res.data)
    }
  } catch (err) {
    console.error('내가 쓴 글 로딩 실패:', err)
    if (err.response?.status === 401) {
      alert('로그인이 필요합니다.')
      router.push({ name: 'login' })
    } else {
      alert('내가 쓴 글을 불러오는데 실패했습니다.')
    }
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
.my-posts-container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.page-title {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 2rem;
}

.board-section {
  margin-bottom: 3rem;
}

.board-section h3 {
  font-size: 1.4rem;
  color: #145c2b;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #145c2b;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.post-item {
  background: white;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 1.2rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.post-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.post-main {
  margin-bottom: 1rem;
}

.post-title {
  font-size: 1.1rem;
  font-weight: 500;
  color: #333;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.post-content {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.post-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: #888;
}

.post-stats {
  display: flex;
  gap: 1rem;
}

.likes, .comments {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.solved-badge {
  background: #145c2b;
  color: white;
  font-size: 0.8rem;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
}

.no-posts {
  text-align: center;
  padding: 2rem;
  color: #666;
  background: #f9f9f9;
  border-radius: 8px;
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}
</style> 