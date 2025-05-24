<template>
    <div class="post-list">
        <div class="header-bar">
            <h2>질문 게시판</h2>
            <router-link :to="{ name: 'questioncreate' }">
                <button class="write-btn">질문하기</button>
            </router-link>
        </div>

        <div v-if="paginatedPosts.length">
            <div v-for="(post, index) in paginatedPosts" :key="post.id" class="post-card">
                <router-link :to="{ name: 'questiondetail', params: { id: post.id } }" class="post-link">
                    <div class="card-row">
                        <div class="no">{{ getPostNumber(index) }}</div>
                        <div class="title">
                            {{ post.title }}
                            <span class="comment-count">({{ post.comments.length }})</span>
                            <span class="solved-badge" v-if="post.is_solved">해결됨</span>
                        </div>
                        <div class="author">{{ post.author }}</div>
                        <div class="date">{{ formatDate(post.created_at) }}</div>
                    </div>
                </router-link>
            </div>
        </div>

        <div v-else class="no-posts">등록된 질문이 없습니다.</div>

        <div v-if="totalPages > 1" class="pagination">
            <button v-for="page in totalPages" :key="page" @click="currentPage = page"
                :class="{ active: currentPage === page }">
                {{ page }}
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

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

onMounted(async () => {
    try {
        const res = await axios.get('/api/v1/posts/question/')
        posts.value = res.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    } catch (err) {
        console.error('질문 목록 조회 실패:', err)
        // 더미 데이터
        posts.value = [
            {
                id: 1,
                title: '주식투자 초보자인데 ETF 추천해주세요',
                content: '안정적인 ETF 위주로 추천 부탁드립니다.',
                created_at: '2025-05-18T14:00:00Z',
                author: '투자초보',
                likes: 5,
                comments: Array(3).fill({}),
                is_solved: true
            },
            {
                id: 2,
                title: '적금 금리 비교 어떻게 하나요?',
                content: '은행마다 금리가 달라서 고민이에요.',
                created_at: '2025-05-17T09:00:00Z',
                author: '머니러버',
                likes: 8,
                comments: Array(5).fill({}),
                is_solved: false
            },
            {
                id: 3,
                title: '주식 차트 보는 법 알려주세요',
                content: '기술적 분석 어떻게 시작하나요?',
                created_at: '2025-05-16T10:30:00Z',
                author: '차트초보',
                likes: 12,
                comments: Array(7).fill({}),
                is_solved: true
            },
            {
                id: 4,
                title: '연말정산 공제 항목 질문',
                content: '올해 바뀐 공제 항목이 있나요?',
                created_at: '2025-05-15T12:00:00Z',
                author: '절세왕',
                likes: 15,
                comments: Array(10).fill({}),
                is_solved: false
            },
            {
                id: 5,
                title: '주식 투자 시작 자금',
                content: '처음 시작할 때 얼마부터 시작하는게 좋을까요?',
                created_at: '2025-05-14T09:00:00Z',
                author: '신입투자자',
                likes: 20,
                comments: Array(12).fill({}),
                is_solved: true
            }
        ].sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
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

.header-bar h2 {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
    color: white;
}

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
    grid-template-columns: 60px 1fr 120px 120px;
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
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.comment-count {
    color: #145c2b;
    font-size: 0.9rem;
}

.solved-badge {
    background: #145c2b;
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
}

.author {
    font-size: 0.9rem;
    color: #444;
    text-align: center;
}

.date {
    font-size: 0.85rem;
    color: #666;
    text-align: right;
}

.no-posts {
    text-align: center;
    padding: 3rem 0;
    color: #666;
    font-size: 1.1rem;
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