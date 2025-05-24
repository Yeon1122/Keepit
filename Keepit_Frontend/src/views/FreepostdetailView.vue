<template>
    <div class="post-detail" v-if="post">
        <router-link :to="{ name: 'freecommunity' }" class="back-link">&gt; 자유 게시판</router-link>

        <div class="post-container">
            <div class="header">
                <h1 class="title">{{ post.title }}</h1>
                <span class="date">{{ formatDate(post.created_at) }}</span>
            </div>
            
            <p class="author">
                작성자: <router-link :to="{ name: 'userpage', params: { userid: post.author_id }}" class="author-name">{{ post.author_nickname }}</router-link>
            </p>

            <div class="content">{{ post.content }}</div>

            <div class="like-actions">
                <div class="like-wrapper" v-if="isAuthenticated">
                    <LikeButton
                        :initial-is-liked="isLiked"
                        :initial-count="post.likes"
                        @update:liked="handlePostLike"
                    />
                </div>
                <div v-else class="like-count">
                    좋아요 {{ post.likes }}개
                </div>

                <!-- 작성자만 볼 수 있는 수정/삭제 버튼 -->
                <div v-if="isAuthenticated && isAuthor" class="post-actions">
                    <button class="btn-edit" @click="handleEdit">수정</button>
                    <button class="btn-delete" @click="handleDelete">삭제</button>
                </div>
            </div>
        </div>

        <hr />

        <div class="comments">
            <h3>댓글 {{ comments.length }}개</h3>
            
            <!-- 로그인한 경우에만 댓글 작성 폼 표시 -->
            <div v-if="isAuthenticated" class="comment-form">
                <input
                    type="text"
                    v-model="newComment"
                    placeholder="댓글을 입력하세요"
                    @keyup.enter="addComment"
                />
                <button class="btn-outline-green" @click="addComment">작성</button>
            </div>
            <div v-else class="login-prompt">
                <p>댓글을 작성하려면 <router-link to="/users/login" class="login-link">로그인</router-link>이 필요합니다.</p>
            </div>

            <!-- 댓글 목록 -->
            <div v-if="comments.length > 0" class="comment-list">
                <div v-for="comment in comments" :key="comment.id" class="comment-item">
                    <div class="comment-content">
                        <p>{{ comment.content }}</p>
                        <div class="comment-info">
                            <span class="comment-author">{{ comment.author_nickname }}</span>
                            <span>{{ formatDate(comment.created_at) }}</span>
                        </div>
                    </div>
                    <!-- 댓글 작성자만 볼 수 있는 삭제 버튼 -->
                    <button 
                        v-if="isAuthenticated && comment.author_id === userId" 
                        class="btn-delete-comment"
                        @click="deleteComment(comment.id)"
                    >
                        삭제
                    </button>
                </div>
            </div>
            <div v-else class="no-comments">
                아직 댓글이 없습니다.
            </div>
        </div>
    </div>

    <div v-else>게시글을 불러오는 중입니다...</div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/users'
import axios from 'axios'
import LikeButton from '@/components/LikeButton.vue'

const route = useRoute()
const router = useRouter()
const postId = route.params.id
const post = ref(null)
const newComment = ref('')
const isLiked = ref(false)

const accountStore = useAccountStore()
const isAuthenticated = computed(() => accountStore.isAuthenticated)
const userId = computed(() => accountStore.user_id)

const formatDate = (iso) => new Date(iso).toLocaleDateString()

const toggleLike = async () => {
    isLiked.value = !isLiked.value
    post.value.likes += isLiked.value ? 1 : -1
    // await axios.post(`http://localhost:8000/api/v1/posts/free/${postId}/like/`) // 실제 좋아요 요청
}

const toggleCommentLike = async (commentId) => {
    const comment = post.value.comments.find(c => c.id === commentId)
    comment.is_liked = !comment.is_liked
    comment.likes += comment.is_liked ? 1 : -1
    // await axios.post(`http://localhost:8000/api/v1/posts/free/${postId}/comments/${commentId}/like/`)
}

const deletePost = async () => {
    if (!confirm('정말 삭제하시겠습니까?')) return
    // await axios.delete(`http://localhost:8000/api/v1/posts/free/${postId}/`)
    alert('삭제 완료')
    router.push({ name: 'freecommunity' })
}

const editPost = () => {
    router.push({ name: 'freepostedit', params: { id: postId } })
}

const goToUserPage = (userid) => {
    router.push({ name: 'userpage', params: { userid } })
}

const submitComment = async () => {
    if (!newComment.value.trim()) return

    const tempComment = {
        id: Date.now(),
        content: newComment.value,
        likes: 0,
        is_liked: false
    }

    post.value.comments.push(tempComment)
    newComment.value = ''

    // await axios.post(`http://localhost:8000/api/v1/posts/free/${postId}/comments/`, {
    //   content: tempComment.content
    // })
}

// 현재 사용자가 글 작성자인지 확인
const isAuthor = computed(() => {
    return post.value && userId.value === post.value.author_id
})

onMounted(async () => {
    // const res = await axios.get(`http://localhost:8000/api/v1/posts/free/${postId}`)
    // post.value = res.data

    post.value = {
        id: postId,
        title: '더미 게시글 제목',
        content: '이것은 더미 게시글의 상세 내용입니다.',
        created_at: '2024-05-01T12:00:00Z',
        author: '홍길동',
        author_id: 'hadmin',
        likes: 5,
        comments: [
            { id: 1, content: '첫 번째 댓글입니다.', likes: 2, is_liked: false },
            { id: 2, content: '좋은 글 감사합니다!', likes: 1, is_liked: true }
        ]
    }
})
</script>


<style scoped>
.post-detail {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1.5rem;
}

.back-link {
    font-size: 0.9rem;
    color: #145c2b;
    text-decoration: none;
    margin-bottom: 1rem;
    display: inline-block;
    transition: color 0.2s ease;
}

.back-link:hover {
    color: #0d3d1d;
}

.post-container {
    background-color: white;
    padding: 2rem;
    border: 1px solid #e0e0e0;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #f0f0f0;
}

.title {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
    color: #1a1a1a;
}

.date {
    font-size: 0.85rem;
    color: #666;
    margin: 0.2rem 0 0 1rem;
    white-space: nowrap;
}

.author {
    margin: 0;
    font-size: 0.95rem;
    color: #444;
    margin-bottom: 1.5rem;
}

.author-name {
    color: #145c2b;
    cursor: pointer;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s ease;
}

.author-name:hover {
    color: #0d3d1d;
    text-decoration: underline;
}

.content {
    margin-top: 1rem;
    white-space: pre-wrap;
    font-size: 1.05rem;
    line-height: 1.7;
    color: #2c2c2c;
}

.like-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 2rem 0;
    padding: 1rem 0;
    border-top: 1px solid #f0f0f0;
}

.like-wrapper,
.comment-like-wrapper {
    display: flex;
    align-items: center;
    gap: 0.7rem;
}

.icon-button.heart {
    background-color: transparent;
    color: #e272c0;
    font-size: 1.3rem;
    border: none;
    padding: 0.5rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.icon-button.heart:hover {
    transform: scale(1.1);
}

.icon-button.heart i {
    transition: color 0.2s ease;
}

.icon-button.heart.active i {
    color: #e272c0;
}

.btn-green {
    background-color: #145c2b;
    color: white;
    border: none;
    padding: 0.4rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    margin-left: 0.5rem;
}

.btn-outline-green {
    background-color: white;
    color: #145c2b;
    border: 1px solid #145c2b;
    padding: 0.3rem 0.8rem;
    font-size: 0.85rem;
    height: 32px;
    border-radius: 6px;
    cursor: pointer;
    margin-left: 0.5rem;
}

.comments {
    margin-top: 2rem;
    font-size: 0.95rem;
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.comments h3 {
    font-size: 1.2rem;
    color: #1a1a1a;
    margin-bottom: 1.2rem;
}

.comment-form {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 1rem 0 1.5rem;
}

.comment-form input {
    flex: 1;
    padding: 0.8rem 1rem;
    font-size: 0.95rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    transition: border-color 0.2s ease;
}

.comment-form input:focus {
    outline: none;
    border-color: #145c2b;
}

.comment-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.95rem;
    padding: 1rem 0;
    border-bottom: 1px solid #f0f0f0;
}

.comment-item:last-child {
    border-bottom: none;
}

.comment-like-wrapper {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.like-count,
.comment-like-count {
    font-size: 0.95rem;
    color: #666;
}

hr {
    border: none;
    height: 1px;
    background-color: #f0f0f0;
    margin: 2rem 0;
}

.post-actions,
.comment-actions {
    display: flex;
    justify-content: flex-end;
    padding: 1rem 0;
}

.login-prompt {
    text-align: center;
    padding: 1rem;
    background-color: #f8f9fa;
    border-radius: var(--radius-md);
    margin: 1rem 0;
}

.login-link {
    color: var(--primary-color);
    text-decoration: none;
    font-weight: 500;
}

.login-link:hover {
    text-decoration: underline;
}

.like-count-only {
    color: var(--text-secondary);
    font-size: 0.9rem;
}
</style>
