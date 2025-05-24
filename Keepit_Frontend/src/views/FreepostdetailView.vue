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
                        :initial-is-liked="post.is_liked"
                        :initial-count="post.likes_count"
                        @update:liked="handlePostLike"
                    />
                </div>
                <div v-else class="like-count">
                    좋아요 {{ post.likes_count }}개
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
            <h3>댓글 {{ comments.length || 0 }}개</h3>
            
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
                            <router-link 
                                :to="{ name: 'userpage', params: { userid: comment.author_id }}" 
                                class="comment-author"
                            >
                                {{ comment.author_nickname }}
                            </router-link>
                            <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                            <div class="comment-like-wrapper" v-if="isAuthenticated">
                                <LikeButton
                                    :initial-is-liked="comment.is_liked"
                                    :initial-count="comment.likes_count"
                                    @update:liked="(newState) => handleCommentLike(comment.id, newState)"
                                    size="small"
                                />
                            </div>
                            <div v-else class="like-count">
                                좋아요 {{ comment.likes_count }}개
                            </div>
                        </div>
                    </div>
                    <!-- 댓글 작성자만 볼 수 있는 삭제 버튼 -->
                    <button 
                        v-if="isAuthenticated && comment.author_id === accountStore.userId" 
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
const comments = ref([])

const accountStore = useAccountStore()
const isAuthenticated = computed(() => accountStore.isAuthenticated)
const userId = computed(() => accountStore.userId)

const formatDate = (iso) => new Date(iso).toLocaleDateString()

// 현재 사용자가 글 작성자인지 확인
const isAuthor = computed(() => {
    return post.value && String(userId.value) === String(post.value.author_id);
})

const handlePostLike = async (newLikedState) => {
    try {
        await axios.post(`http://127.0.0.1:8000/api/v1/community/free/${postId}/like/`, {}, {
            headers: {
                Authorization: `Token ${accountStore.token}`
            }
        })
        isLiked.value = newLikedState
        if (post.value) {
            post.value.likes += newLikedState ? 1 : -1
        }
    } catch (err) {
        console.error('좋아요 처리 실패:', err)
        if (err.response?.status === 401) {
            alert('로그인이 필요합니다.')
            router.push({ name: 'login' })
        }
    }
}

const handleEdit = () => {
    if (!isAuthor.value) {
        alert('자신의 게시글만 수정할 수 있습니다.')
        return
    }
    router.push({ name: 'freepostedit', params: { id: postId } })
}

const handleDelete = async () => {
    if (!isAuthor.value) {
        alert('자신의 게시글만 삭제할 수 있습니다.')
        return
    }
    
    if (!confirm('정말 삭제하시겠습니까?')) return
    
    try {
        await axios.delete(`http://127.0.0.1:8000/api/v1/community/free/${postId}/`, {
            headers: {
                Authorization: `Token ${accountStore.token}`
            }
        })
        alert('게시글이 삭제되었습니다.')
        router.push({ name: 'freecommunity' })
    } catch (err) {
        console.error('게시글 삭제 실패:', err)
        if (err.response?.status === 401) {
            alert('로그인이 필요합니다.')
            router.push({ name: 'login' })
        } else {
            alert('게시글 삭제 중 오류가 발생했습니다.')
        }
    }
}

const addComment = async () => {
    if (!newComment.value.trim()) return
    if (!isAuthenticated.value) {
        alert('로그인이 필요합니다.')
        router.push({ name: 'login' })
        return
    }

    try {
        const response = await axios.post(
            `http://127.0.0.1:8000/api/v1/community/free/${postId}/comments/`,
            { content: newComment.value },
            {
                headers: {
                    Authorization: `Token ${accountStore.token}`,
                    'Content-Type': 'application/json'
                }
            }
        )
        comments.value.push(response.data)
        newComment.value = ''
    } catch (err) {
        console.error('댓글 작성 실패:', err)
        if (err.response?.status === 401) {
            alert('로그인이 필요합니다.')
            router.push({ name: 'login' })
        } else {
            alert('댓글 작성 중 오류가 발생했습니다.')
        }
    }
}

const deleteComment = async (commentId) => {
    try {
        await axios.delete(
            `http://127.0.0.1:8000/api/v1/community/free/${postId}/comments/${commentId}/`,
            {
                headers: {
                    Authorization: `Token ${accountStore.token}`
                }
            }
        )
        comments.value = comments.value.filter(c => c.id !== commentId)
    } catch (err) {
        console.error('댓글 삭제 실패:', err)
        if (err.response?.status === 401) {
            alert('로그인이 필요합니다.')
            router.push({ name: 'login' })
        } else {
            alert('댓글 삭제 중 오류가 발생했습니다.')
        }
    }
}

const handleCommentLike = async (commentId, newState) => {
    try {
        await axios.post(
            `http://127.0.0.1:8000/api/v1/community/free/${postId}/comments/${commentId}/like/`,
            {},
            {
                headers: {
                    Authorization: `Token ${accountStore.token}`
                }
            }
        )
        comments.value = comments.value.map(c =>
            c.id === commentId 
                ? { 
                    ...c, 
                    is_liked: newState,
                    likes_count: newState ? c.likes_count + 1 : c.likes_count - 1 
                } 
                : c
        )
    } catch (err) {
        console.error('댓글 좋아요 처리 실패:', err)
        if (err.response?.status === 401) {
            alert('로그인이 필요합니다.')
            router.push({ name: 'login' })
        } else {
            alert('댓글 좋아요 처리 중 오류가 발생했습니다.')
        }
    }
}

onMounted(async () => {
    try {
        const headers = accountStore.isAuthenticated
            ? { Authorization: `Token ${accountStore.token}` }
            : {}

        const [postRes, commentsRes] = await Promise.all([
            axios.get(`http://127.0.0.1:8000/api/v1/community/free/${postId}/`, { headers }),
            axios.get(`http://127.0.0.1:8000/api/v1/community/free/${postId}/comments/`, { headers })
        ])
        
        post.value = postRes.data
        comments.value = commentsRes.data
        isLiked.value = post.value.is_liked || false
        
    } catch (err) {
        console.error('게시글 로딩 실패:', err)
        alert('게시글을 불러오는데 실패했습니다.')
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
    align-items: flex-start;
    margin: 2rem 0 1rem;
    padding: 2rem 0 0;
    border-top: 1px solid #f0f0f0;
}

.like-wrapper {
    margin-top: 0.5rem;
}

.post-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
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

.comment-info {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 0.5rem;
    font-size: 0.9rem;
    color: #666;
}

.comment-author {
    color: #145c2b;
    font-weight: 500;
    text-decoration: none;
}

.comment-author:hover {
    text-decoration: underline;
}

.comment-date {
    color: #888;
}

.comment-like-wrapper {
    display: flex;
    align-items: center;
    gap: 0.5rem;
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

.btn-delete-comment {
    background: none;
    border: none;
    color: #dc3545;
    font-size: 0.9rem;
    cursor: pointer;
    padding: 0.3rem 0.6rem;
    border-radius: 4px;
    transition: all 0.2s ease;
}

.btn-delete-comment:hover {
    background-color: #fff5f5;
}

.btn-edit {
    background: #145c2b;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    margin-right: 0.5rem;
    transition: all 0.2s ease;
}

.btn-edit:hover {
    background: #0d3d1d;
}

.btn-delete {
    background: #dc3545;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.2s ease;
}

.btn-delete:hover {
    background: #c82333;
}
</style>
