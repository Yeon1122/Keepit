<template>
    <div class="post-list">
        <div class="header-bar">
            <h2>자유 게시판</h2>
            <button v-if="isAuthenticated" class="write-btn" @click="goToWrite">글쓰기</button>
        </div>

        <div v-if="posts.length > 0">
            <div v-for="(post, index) in paginatedPosts" :key="post.id" class="post-card">
                <router-link :to="{ name: 'freepostdetail', params: { id: post.id } }" class="post-link">
                    <div class="card-row">
                        <div class="no">{{ getPostNumber(index) }}</div>
                        <div class="title">
                            {{ post.title }}
                        </div>
                        <div class="info-section">
                            <span class="like-count">
                                <i class="fas fa-thumbs-up"></i> {{ post.likes_count }}
                            </span>
                            <span class="comment-count">
                                <i class="fas fa-comment"></i> {{ post.comments.length }}
                            </span>
                            <span class="author">
                                <i class="fas fa-user"></i> {{ post.author_nickname }}
                            </span>
                            <span class="date">{{ formatDate(post.created_at) }}</span>
                        </div>
                    </div>
                </router-link>
            </div>

            <!-- ✅ 페이지네이션 -->
            <div v-if="totalPages > 1" class="pagination">
                <button v-for="page in totalPages" :key="page" @click="currentPage = page"
                    :class="{ active: currentPage === page }">
                    {{ page }}
                </button>
            </div>
        </div>

        <div v-else class="no-posts">
            <p>아직 작성된 게시글이 없습니다.</p>
            <p v-if="isAuthenticated" class="write-prompt">첫 게시글을 작성해보세요!</p>
            <p v-else class="login-prompt">게시글을 작성하려면 로그인이 필요합니다.</p>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/users'
import axios from 'axios'

const accountStore = useAccountStore()
const isAuthenticated = computed(() => accountStore.isAuthenticated)

const posts = ref([])
const currentPage = ref(1)
const itemsPerPage = 10

const formatDate = (iso) => new Date(iso).toLocaleDateString()

const paginatedPosts = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage
    return posts.value.slice(start, start + itemsPerPage)
})

const totalPages = computed(() =>
    Math.ceil(posts.value.length / itemsPerPage)
)

const getPostNumber = (index) => {
    return (posts.value.length - 1) - ((currentPage.value - 1) * itemsPerPage + index) + 1
}

const router = useRouter()

const goToWrite = () => {
    router.push({ name: 'freepostcreate' })
}

onMounted(async () => {
    try {
        const headers = accountStore.isAuthenticated
            ? { Authorization: `Token ${accountStore.token}` }
            : {}
            
        const res = await axios.get('http://127.0.0.1:8000/api/v1/community/free/', { headers })
        posts.value = res.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    } catch (err) {
        console.error('❌ 게시글 조회 실패', err)
        alert('게시글을 불러오는데 실패했습니다.')
        posts.value = []
    }
})
</script>

<style scoped>
.post-list {
    max-width: 1000px;
    margin: 2rem auto;
    padding: 0 1.5rem;
    font-family: 'Pretendard', sans-serif;
}

.header-bar {
    background-color: #145c2b;
    color: white;
    padding: 1.5rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 12px rgba(20, 92, 43, 0.1);
}

.header-bar h2 {    font-size: 1.5rem;    font-weight: 600;    margin: 0;    color: white;}

.write-btn {
    background: white;
    color: #145c2b;
    padding: 0.6rem 1.4rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.95rem;
    transition: all 0.2s ease;
}

.write-btn:hover {
    background-color: #f8f8f8;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.post-card {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    margin-bottom: 0.8rem;
    transition: all 0.2s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.post-card:hover {
    border-color: #145c2b;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(20, 92, 43, 0.1);
}

.post-link {
    text-decoration: none;
    color: inherit;
    display: block;
    padding: 1.2rem 1.5rem;
}

.card-row {
    display: grid;
    grid-template-columns: 60px 1fr 300px;
    align-items: center;
    gap: 1.5rem;
}

.no {
    font-size: 0.9rem;
    color: #666;
    text-align: center;
}

.title {
    font-size: 1rem;
    color: #1a1a1a;
    font-weight: 500;
}

.info-section {
    display: flex;
    align-items: center;
    gap: 1rem;
    justify-content: flex-end;
}

.like-count {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.9rem;
    color: #ff4b4b;
}

.like-count i {
    color: #ff4b4b;
}

.comment-count, .author, .date {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.9rem;
}

.author {
    color: #145c2b;
    font-weight: 500;
}

.date {
    color: #666;
}

.no-posts {
    text-align: center;
    padding: 3rem 0;
    color: #666;
    background: white;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    margin: 2rem 0;
}

.no-posts p {
    margin: 0.5rem 0;
    font-size: 1.1rem;
}

.write-prompt {
    color: #145c2b;
    font-weight: 500;
}

.login-prompt {
    font-size: 0.9rem;
    color: #888;
}

.pagination {
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
    gap: 0.5rem;
}

.pagination button {
    padding: 0.5rem 1rem;
    border: 1px solid #ccc;
    background-color: white;
    color: #145c2b;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s;
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.pagination button:hover {
    background-color: #f0f0f0;
    border-color: #145c2b;
}

.pagination button.active {
    background-color: #145c2b;
    color: white;
    border-color: #145c2b;
}
</style>
