<template>
    <div class="post-detail" v-if="post">
        <router-link :to="{ name: 'questioncommunity' }" class="back-link">&gt; 질문 게시판</router-link>

        <div class="post-box">
            <div class="header">
                <div class="title-wrapper">
                    <h2 class="title">{{ post.title }}</h2>
                    <span class="solved-badge" v-if="post.is_solved">해결됨</span>
                </div>
                <p class="date">{{ formatDate(post.created_at) }}</p>
            </div>
            <p class="author">작성자: <span @click="goToUserPage(post.author_id)" class="author-name">{{ post.author }}</span></p>
            <div class="content">{{ post.content }}</div>
        </div>

        <div class="like-actions">
            <div class="like-wrapper">
                <LikeButton
                    :initial-is-liked="isLiked"
                    :initial-count="post.likes"
                    @update:liked="handlePostLike"
                />
            </div>
            <div class="action-buttons">
                <button class="btn-solve" v-if="!post.is_solved" @click="markAsSolved">해결 완료</button>
                <button class="btn-green" @click="editPost">수정</button>
                <button class="btn-green" @click="deletePost">삭제</button>
            </div>
        </div>

        <hr />

        <div class="comments">
            <h3>답변 ({{ post.comments?.length || 0 }})</h3>
            <form @submit.prevent="submitComment" class="comment-form">
                <input v-model="newComment" placeholder="답변을 입력하세요" />
                <button type="submit" class="btn-outline-green">등록</button>
            </form>

            <ul v-if="post.comments?.length">
                <li v-for="comment in post.comments" :key="comment.id" class="comment-item">
                    <div class="comment-content">
                        <p>{{ comment.content }}</p>
                        <div class="comment-info">
                            <span class="comment-author">{{ comment.author }}</span>
                            <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
                        </div>
                    </div>
                    <div class="comment-like-wrapper">
                        <LikeButton
                            :initial-is-liked="comment.is_liked"
                            :initial-count="comment.likes"
                            @update:liked="(value) => handleCommentLike(comment.id, value)"
                        />
                    </div>
                </li>
            </ul>
            <div v-else class="no-comments">아직 답변이 없습니다.</div>
        </div>
    </div>

    <div v-else class="loading">질문을 불러오는 중입니다...</div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import LikeButton from '@/components/LikeButton.vue'
import { useAccountStore } from '@/stores/users'

const route = useRoute()
const router = useRouter()
const postId = route.params.id
const post = ref(null)
const newComment = ref('')
const isLiked = ref(false)

const accountStore = useAccountStore()
const isAuthenticated = computed(() => accountStore.isAuthenticated)
const userId = computed(() => accountStore.user_id)

const isAuthor = computed(() => {
    return post.value && userId.value === post.value.author_id
})

const formatDate = (iso) => new Date(iso).toLocaleDateString()

const toggleLike = async () => {
    try {
        // await axios.post(`/api/v1/posts/questions/${postId}/like/`)
        isLiked.value = !isLiked.value
        post.value.likes += isLiked.value ? 1 : -1
    } catch (err) {
        console.error('좋아요 처리 실패:', err)
    }
}

const toggleCommentLike = async (commentId) => {
    try {
        // await axios.post(`/api/v1/posts/question/${postId}/comments/${commentId}/like/`)
        const comment = post.value.comments.find(c => c.id === commentId)
        if (comment) {
            comment.is_liked = !comment.is_liked
            comment.likes += comment.is_liked ? 1 : -1
        }
    } catch (err) {
        console.error('댓글 좋아요 처리 실패:', err)
    }
}

const markAsSolved = async () => {
    try {
        // await axios.put(`/api/v1/posts/question/${postId}/`, {
        //     ...post.value,
        //     is_solved: true
        // })
        post.value.is_solved = true
    } catch (err) {
        console.error('해결 완료 처리 실패:', err)
    }
}

const deletePost = async () => {
    if (!confirm('정말 삭제하시겠습니까?')) return
    try {
        // await axios.delete(`/api/v1/posts/question/${postId}/`)
        alert('삭제되었습니다.')
        router.push({ name: 'questioncommunity' })
    } catch (err) {
        console.error('게시글 삭제 실패:', err)
        alert('삭제 중 오류가 발생했습니다.')
    }
}

const editPost = () => {
    router.push({ name: 'questionedit', params: { id: postId } })
}

const goToUserPage = (userid) => {
    router.push({ name: 'userpage', params: { userid } })
}

const submitComment = async () => {
    if (!newComment.value.trim()) return

    try {
        // await axios.post(`/api/v1/posts/question/${postId}/comments/`, {
        //     content: newComment.value
        // })
        
        const tempComment = {
            id: Date.now(),
            content: newComment.value,
            author: '현재 사용자',
            created_at: new Date().toISOString(),
            likes: 0,
            is_liked: false
        }

        if (!post.value.comments) {
            post.value.comments = []
        }
        post.value.comments.push(tempComment)
        newComment.value = ''
    } catch (err) {
        console.error('답변 작성 실패:', err)
        alert('답변 작성 중 오류가 발생했습니다.')
    }
}

onMounted(async () => {
    try {
        // const res = await axios.get(`/api/v1/posts/question/${postId}`)
        // post.value = res.data

        // 더미 데이터
        post.value = {
            id: postId,
            title: '주식투자 초보자인데 ETF 추천해주세요',
            content: '안정적인 ETF 위주로 추천 부탁드립니다. 월 100만원 정도 투자할 예정입니다.',
            created_at: '2024-05-01T12:00:00Z',
            author: '투자초보',
            author_id: 'beginner',
            likes: 5,
            is_solved: false,
            comments: [
                {
                    id: 1,
                    content: 'KODEX 200이나 TIGER 미국S&P500 ETF를 추천드립니다. 안정적이고 수수료도 낮습니다.',
                    author: '투자전문가',
                    created_at: '2024-05-01T13:00:00Z',
                    likes: 3,
                    is_liked: false
                },
                {
                    id: 2,
                    content: '분산투자를 위해 여러 ETF에 나눠서 투자하시는 것을 추천드립니다.',
                    author: '자산관리사',
                    created_at: '2024-05-01T14:00:00Z',
                    likes: 2,
                    is_liked: true
                }
            ]
        }
    } catch (err) {
        console.error('질문 조회 실패:', err)
        post.value = null
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

.post-box {
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

.title-wrapper {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.title {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
    color: #1a1a1a;
}

.solved-badge {
    background: #145c2b;
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 6px;
    font-size: 0.9rem;
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
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.95rem;
    margin-left: 0.5rem;
    transition: all 0.2s ease;
}

.btn-green:hover {
    background: #0d3d1d;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(20, 92, 43, 0.2);
}

.btn-solve {
    background-color: #1a73e8;
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.95rem;
    margin-right: 0.5rem;
    transition: all 0.2s ease;
}

.btn-solve:hover {
    background: #1557b0;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(26, 115, 232, 0.2);
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
    transition: all 0.2s ease;
}

.comment-form input:focus {
    outline: none;
    border-color: #145c2b;
    box-shadow: 0 0 0 3px rgba(20, 92, 43, 0.1);
}

.btn-outline-green {
    background-color: white;
    color: #145c2b;
    border: 1px solid #145c2b;
    padding: 0.8rem 1.5rem;
    font-size: 0.95rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn-outline-green:hover {
    background: #145c2b;
    color: white;
}

.comment-item {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 1rem 0;
    border-bottom: 1px solid #f0f0f0;
}

.comment-item:last-child {
    border-bottom: none;
}

.comment-content {
    flex: 1;
    margin-right: 1rem;
}

.comment-content p {
    margin: 0 0 0.5rem 0;
    line-height: 1.6;
}

.comment-info {
    display: flex;
    gap: 1rem;
    font-size: 0.85rem;
    color: #666;
}

.comment-author {
    color: #145c2b;
    font-weight: 500;
}

hr {
    border: none;
    height: 1px;
    background-color: #f0f0f0;
    margin: 2rem 0;
}

.loading {
    text-align: center;
    padding: 3rem;
    color: #666;
    font-size: 1.1rem;
}

.no-comments {
    text-align: center;
    padding: 2rem 0;
    color: #666;
    font-size: 1rem;
}

.post-actions,
.comment-actions {
    display: flex;
    justify-content: flex-end;
    padding: 1rem 0;
}

.status-display {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.status-solved {
    color: #28a745;
    font-weight: 500;
}
</style> 