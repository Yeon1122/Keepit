<template>
    <div class="post-detail" v-if="post">
        <router-link :to="{ name: 'questioncommunity' }" class="back-link">&gt; 질문 게시판</router-link>

        <div class="post-box">
            <div class="header">
                <div class="title-wrapper">
                    <h2 class="title">{{ post.title }}</h2>
                    <span class="solved-badge" v-if="post.is_solved">해결됨</span>
                </div>
                <div class="post-info">
                    <p class="author">
                        작성자: <router-link :to="{ name: 'userpage', params: { userid: post.author_id }}" class="author-name">{{ post.author_nickname }}</router-link>
                    </p>
                    <p class="date">{{ formatDate(post.created_at) }}</p>
                </div>
            </div>
            <div class="content">{{ post.content }}</div>
            
            <div class="post-footer">
                <div class="like-wrapper" v-if="isAuthenticated">
                    <LikeButton
                        :initial-is-liked="isLiked"
                        :initial-count="post.likes"
                        @update:liked="handlePostLike"
                    />
                </div>
                <div v-else class="like-count">
                    좋아요 {{ post.likes_count }}개
                </div>

                <div v-if="isAuthenticated && isAuthor" class="action-buttons">
                    <button class="btn-solve" v-if="!post.is_solved" @click="markAsSolved">해결 완료</button>
                    <button class="btn-edit" @click="editPost">수정</button>
                    <button class="btn-delete" @click="deletePost">삭제</button>
                </div>
            </div>
        </div>

        <div class="comments-section">
            <h3>답변 ({{ comments.length || 0 }})</h3>
            
            <form v-if="isAuthenticated" @submit.prevent="submitComment" class="comment-form">
                <div class="input-wrapper">
                    <textarea 
                        v-model="newComment" 
                        placeholder="답변을 입력하세요" 
                        rows="3"
                        class="comment-input"
                    ></textarea>
                    <button type="submit" class="btn-submit">답변 등록</button>
                </div>
            </form>

            <div class="comments-list">
                <div v-if="comments.length" class="comment-items">
                    <div v-for="comment in comments" :key="comment.id" class="comment-item">
                        <div class="comment-content">
                            <p class="comment-text">{{ comment.content }}</p>
                            <div class="comment-info">
                                <router-link :to="{ name: 'userpage', params: { userid: comment.author_id }}" class="comment-author">
                                    {{ comment.author_nickname }}
                                </router-link>
                                <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                            </div>
                        </div>
                        
                        <div class="comment-actions">
                            <div class="comment-like-wrapper" v-if="isAuthenticated">
                                <LikeButton
                                    :initial-is-liked="comment.is_liked"
                                    :initial-count="comment.likes_count"
                                    @update:liked="(value) => handleCommentLike(comment.id, value)"
                                    size="small"
                                />
                            </div>
                            <button 
                                v-if="isAuthenticated && comment.author_id === accountStore.userId" 
                                class="btn-delete-comment"
                                @click="deleteComment(comment.id)"
                            >
                                삭제
                            </button>
                        </div>
                    </div>
                </div>
                <div v-else class="no-comments">아직 답변이 없습니다.</div>
            </div>
        </div>
    </div>

    <div v-else class="loading">
        <div class="loading-spinner"></div>
        <p>질문을 불러오는 중입니다...</p>
    </div>
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

const isAuthor = computed(() => {
    console.log('userId:', userId.value, 'author_id:', post.value?.author_id);
    return post.value && String(userId.value) === String(post.value.author_id);
})

const formatDate = (iso) => new Date(iso).toLocaleDateString()

const handlePostLike = async (newLikedState) => {
    try {
        await axios.post(`http://127.0.0.1:8000/api/v1/community/question/${postId}/like/`, {}, {
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

const handleCommentLike = async (commentId, newState) => {
    try {
        await axios.post(
            `http://127.0.0.1:8000/api/v1/community/question/${postId}/comments/${commentId}/like/`,
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

const deleteComment = async (commentId) => {
    if (!confirm('정말로 이 답변을 삭제하시겠습니까?')) {
        return
    }

    try {
        await axios.delete(
            `http://127.0.0.1:8000/api/v1/community/question/${postId}/comments/${commentId}/`,
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

const markAsSolved = async () => {
    try {
        await axios.put(`http://127.0.0.1:8000/api/v1/community/question/${postId}/`, {
            ...post.value,
            is_solved: true
        }, {
            headers: {
                Authorization: `Token ${accountStore.token}`
            }
        })
        post.value.is_solved = true
    } catch (err) {
        console.error('해결 완료 처리 실패:', err)
    }
}

const deletePost = async () => {
    if (!confirm('정말로 이 게시글을 삭제하시겠습니까?')) {
        return
    }

    try {
        await axios.delete(
            `http://127.0.0.1:8000/api/v1/community/question/${postId}/`,
            {
                headers: {
                    Authorization: `Token ${accountStore.token}`
                }
            }
        )
        alert('게시글이 삭제되었습니다.')
        router.push({ name: 'questioncommunity' })
    } catch (err) {
        console.error('게시글 삭제 실패:', err)
        if (err.response?.status === 401) {
            alert('로그인이 필요합니다.')
            router.push({ name: 'login' })
        } else if (err.response?.status === 403) {
            alert('자신의 게시글만 삭제할 수 있습니다.')
        } else {
            alert('게시글 삭제 중 오류가 발생했습니다.')
        }
    }
}

const editPost = () => {
    if (!isAuthor.value) {
        alert('자신의 게시글만 수정할 수 있습니다.')
        return
    }
    router.push({ name: 'questionedit', params: { id: postId } })
}

const submitComment = async () => {
    if (!newComment.value.trim()) return
    if (!isAuthenticated.value) {
        alert('로그인이 필요합니다.')
        router.push({ name: 'login' })
        return
    }

    try {
        const response = await axios.post(
            `http://127.0.0.1:8000/api/v1/community/question/${postId}/comments/`,
            { content: newComment.value },
            {
                headers: {
                    Authorization: `Token ${accountStore.token}`,
                    'Content-Type': 'application/json'
                }
            }
        )
        comments.value.unshift(response.data)
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

onMounted(async () => {
    try {
        const headers = accountStore.isAuthenticated
            ? { Authorization: `Token ${accountStore.token}` }
            : {}

        const [postRes, commentsRes] = await Promise.all([
            axios.get(`http://127.0.0.1:8000/api/v1/community/question/${postId}/`, { headers }),
            axios.get(`http://127.0.0.1:8000/api/v1/community/question/${postId}/comments/`, { headers })
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
    margin: 3rem auto;
    padding: 0 1.5rem;
}

.back-link {
    font-size: 0.95rem;
    color: #145c2b;
    text-decoration: none;
    margin-bottom: 1.5rem;
    display: inline-block;
    transition: color 0.2s ease;
    padding: 0.5rem 0;
}

.back-link:hover {
    color: #0d3d1d;
}

.post-box {
    background-color: white;
    padding: 2.5rem;
    border: 1px solid #e0e0e0;
    border-radius: 16px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
}

.header {
    margin-bottom: 2rem;
}

.title-wrapper {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    margin-bottom: 1.5rem;
}

.title {
    margin: 0;
    font-size: 1.8rem;
    font-weight: 600;
    color: #1a1a1a;
    line-height: 1.4;
}

.solved-badge {
    background-color: #145c2b;
    color: white;
    padding: 0.4rem 1rem;
    border-radius: 20px;
    font-size: 0.95rem;
    font-weight: 500;
}

.post-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #f0f0f0;
}

.author {
    margin: 0;
    font-size: 1rem;
    color: #444;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.author-name {
    color: #145c2b;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s ease;
    padding: 0.2rem 0;
}

.author-name:hover {
    color: #0d3d1d;
    text-decoration: underline;
}

.date {
    font-size: 0.9rem;
    color: #666;
    margin: 0;
}

.content {
    margin: 2rem 0;
    white-space: pre-wrap;
    font-size: 1.1rem;
    line-height: 1.8;
    color: #2c2c2c;
}

.post-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 2.5rem;
    padding-top: 2rem;
    border-top: 1px solid #f0f0f0;
}

.action-buttons {
    display: flex;
    gap: 0.8rem;
}

.btn-solve,
.btn-edit,
.btn-delete {
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn-solve {
    background-color: #145c2b;
    color: white;
    border: none;
}

.btn-solve:hover {
    background-color: #0d3d1d;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(20, 92, 43, 0.2);
}

.btn-edit {
    background: #145c2b;
    color: white;
    border: none;
}

.btn-edit:hover {
    background: #0d3d1d;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(20, 92, 43, 0.2);
}

.btn-delete {
    background: white;
    color: #dc3545;
    border: 1px solid #dc3545;
}

.btn-delete:hover {
    background: #dc3545;
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(220, 53, 69, 0.2);
}

.comments-section {
    background: white;
    padding: 2.5rem;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
    border: 1px solid #e0e0e0;
}

.comments-section h3 {
    font-size: 1.3rem;
    color: #1a1a1a;
    margin: 0 0 2rem 0;
    font-weight: 600;
}

.comment-form {
    margin-bottom: 2.5rem;
}

.input-wrapper {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
}

.comment-input {
    flex: 1;
    padding: 1.2rem;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    font-size: 1rem;
    resize: vertical;
    min-height: 100px;
    transition: all 0.2s ease;
    line-height: 1.6;
}

.comment-input:focus {
    outline: none;
    border-color: #145c2b;
    box-shadow: 0 0 0 3px rgba(20, 92, 43, 0.1);
}

.btn-submit {
    padding: 0.8rem 1.8rem;
    background: #145c2b;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 500;
    transition: all 0.2s ease;
    white-space: nowrap;
    height: fit-content;
}

.btn-submit:hover {
    background: #0d3d1d;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(20, 92, 43, 0.2);
}

.comment-items {
    border-top: 1px solid #f0f0f0;
}

.comment-item {
    padding: 2rem 0;
    border-bottom: 1px solid #f0f0f0;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 2rem;
}

.comment-item:first-child {
    padding-top: 2rem;
}

.comment-item:last-child {
    border-bottom: none;
}

.comment-content {
    flex: 1;
}

.comment-text {
    margin: 0 0 1rem 0;
    font-size: 1rem;
    line-height: 1.7;
    color: #2c2c2c;
}

.comment-info {
    display: flex;
    gap: 1.2rem;
    align-items: center;
}

.comment-author {
    color: #145c2b;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.2s ease;
}

.comment-author:hover {
    color: #0d3d1d;
    text-decoration: underline;
}

.comment-date {
    font-size: 0.9rem;
    color: #666;
}

.comment-actions {
    display: flex;
    gap: 1.2rem;
    align-items: center;
}

.btn-delete-comment {
    background: none;
    border: none;
    color: #dc3545;
    font-size: 0.95rem;
    cursor: pointer;
    padding: 0.4rem 0.8rem;
    transition: all 0.2s ease;
    border-radius: 6px;
}

.btn-delete-comment:hover {
    background-color: rgba(220, 53, 69, 0.1);
}

.no-comments {
    text-align: center;
    padding: 3rem 0;
    color: #666;
    font-size: 1.1rem;
}

.loading {
    text-align: center;
    padding: 4rem;
    color: #666;
}

.loading-spinner {
    border: 3px solid #f3f3f3;
    border-top: 3px solid #145c2b;
    border-radius: 50%;
    width: 48px;
    height: 48px;
    animation: spin 1s linear infinite;
    margin: 0 auto 1.5rem;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.like-count {
    color: #666;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
</style> 