<template>
    <div class="post-detail" v-if="post">
        <router-link :to="{ name: 'freecommunity' }" class="back-link">&gt; 자유 게시판</router-link>

        <div class="post-box">
            <div class="header">
                <h2 class="title">{{ post.title }}</h2>
                <p class="date">{{ formatDate(post.created_at) }}</p>
            </div>
            <p class="author">작성자: <span @click="goToUserPage(post.author_id)" class="author-name">{{ post.author
                    }}</span></p>
            <div class="content">{{ post.content }}</div>
        </div>

        <div class="like-actions">
            <div class="like-wrapper">
                <button @click="toggleLike" class="icon-button heart" :class="{ active: isLiked }">
                    <i :class="[isLiked ? 'fa-solid' : 'fa-regular', 'fa-heart']"></i>
                </button>
                <span class="like-count">공감 {{ post.likes }}</span>
            </div>
            <div class="action-buttons">
                <button class="btn-green" @click="editPost">수정</button>
                <button class="btn-green" @click="deletePost">삭제</button>
            </div>
        </div>

        <hr />

        <div class="comments">
            <h3>댓글 ({{ post.comments.length }})</h3>
            <form @submit.prevent="submitComment" class="comment-form">
                <input v-model="newComment" placeholder="댓글을 입력하세요" />
                <button type="submit" class="btn-outline-green">등록</button>
            </form>

            <ul>
                <li v-for="comment in post.comments" :key="comment.id" class="comment-item">
                    <p>{{ comment.content }}</p>
                    <div class="comment-like-wrapper">
                        <button class="icon-button heart" @click="toggleCommentLike(comment.id)"
                            :class="{ active: comment.is_liked }">
                            <i :class="[comment.is_liked ? 'fa-solid' : 'fa-regular', 'fa-heart']"></i>
                        </button>
                        <span class="comment-like-count">{{ comment.likes }}</span>
                    </div>
                </li>
            </ul>
        </div>
    </div>

    <div v-else>게시글을 불러오는 중입니다...</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const postId = route.params.id
const post = ref(null)
const newComment = ref('')
const isLiked = ref(false)

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
    max-width: 720px;
    margin: 0 auto;
    padding: 1rem;
}

.back-link {
    font-size: 0.9rem;
    color: #145c2b;
    text-decoration: none;
    margin-bottom: 0.5rem;
    display: inline-block;
}

.post-box {
    background-color: #f9f9f9;
    padding: 1rem 1.5rem;
    border: 1px solid #ddd;
    border-radius: 12px;
    margin-bottom: 1rem;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.3rem;
}

.title {
    margin: 0;
    font-size: 1.25rem;
}

.date {
    font-size: 0.85rem;
    color: #888;
    margin: 0.2rem 0 0 1rem;
    white-space: nowrap;
}

.author {
    margin: 0;
    font-size: 0.9rem;
    color: #333;
    margin-bottom: 0.5rem;
}

.author-name {
    color: #145c2b;
    cursor: pointer;
    text-decoration: underline;
}

.content {
    margin-top: 0.2rem;
    white-space: pre-wrap;
    font-size: 1rem;
    line-height: 1.6;
}

.like-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.like-wrapper,
.comment-like-wrapper {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.icon-button.heart {
    background-color: transparent;
    color: #e272c0;
    font-size: 1.2rem;
    border: none;
    padding: 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
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
    margin-top: 1.5rem;
    font-size: 0.8rem;
    background-color: #fcfcfc;
    border: 1px solid #eee;
    border-radius: 10px;
    padding: 0.8rem 1rem;
}

.comment-form {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 0.5rem;
    margin: 0.5rem 0 0.8rem;
}

.comment-form input {
    width: 75%;
    padding: 0.3rem 0.6rem;
    font-size: 0.8rem;
    height: 28px;
    border: 1px solid #ccc;
    border-radius: 6px;
}

.comment-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.8rem;
    padding: 0.2rem 0;
    border-bottom: 1px solid #eee;
}

.comment-like-wrapper {
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
</style>
