<template>
    <div class="post-list">
        <div class="header-bar">
            <h2>자유 게시판</h2>
            <button v-if="isAuthenticated" class="write-btn" @click="goToWrite">글쓰기</button>
        </div>

        <div v-if="paginatedPosts.length">
            <div v-for="(post, index) in paginatedPosts" :key="post.id" class="post-card">
                <router-link :to="{ name: 'freepostdetail', params: { id: post.id } }" class="post-link">
                    <div class="card-row">
                        <div class="no">{{ getPostNumber(index) }}</div>
                        <div class="title">
                            {{ post.title }}
                            <span class="comment-count">({{ post.comments.length }})</span>
                        </div>
                        <div class="author">{{ post.author }}</div>
                        <div class="date">{{ formatDate(post.created_at) }}</div>
                    </div>
                </router-link>
            </div>
        </div>

        <div v-else class="no-posts">게시글이 없습니다.</div>

        <!-- ✅ 페이지네이션 -->
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
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/users'
// import axios from 'axios'

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

// ✅ 더미 데이터 삽입 + 최신순 정렬
onMounted(async () => {
    // try {
    //   const res = await axios.get('http://127.0.0.1:8000/api/v1/posts/free/')
    //   posts.value = res.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    // } catch (err) {
    //   console.error('❌ 게시글 조회 실패', err)
    // }

    posts.value = [
        {
            id: 1,
            title: '주식 투자 초보자를 위한 팁',
            content: '주식 투자를 처음 시작하시는 분들을 위한 몇 가지 조언을 공유드립니다...',
            created_at: '2025-05-18T14:00:00Z',
            author: '투자마스터',
            likes: 15,
            comments: Array(8).fill({})
        },
        {
            id: 2,
            title: '적금 vs 주식 투자, 어떤 것이 더 좋을까요?',
            content: '월 100만원으로 시작하는 재테크 방법 비교...',
            created_at: '2025-05-19T09:00:00Z',
            author: '하연',
            likes: 22,
            comments: Array(12).fill({})
        },
        {
            id: 3,
            title: '요즘 HOT한 ETF 추천',
            content: '안정적인 수익을 위한 ETF 포트폴리오...',
            author: '주식왕',
            created_at: '2025-05-17T10:30:00Z',
            likes: 18,
            comments: Array(6).fill({})
        },
        {
            id: 4,
            title: '월급 관리의 기술',
            content: '효율적인 지출 관리와 저축 방법...',
            author: '자산관리전문가',
            created_at: '2025-05-16T12:00:00Z',
            likes: 25,
            comments: Array(15).fill({})
        },
        {
            id: 5,
            title: '2025년 금리 전망',
            content: '올해의 금리 동향과 향후 전망...',
            author: '경제분석가',
            created_at: '2025-05-15T09:00:00Z',
            likes: 30,
            comments: Array(20).fill({})
        },
        {
            id: 6,
            title: '주식 차트 보는 법',
            content: '기술적 분석의 기초...',
            author: '차트마스터',
            created_at: '2025-05-14T08:00:00Z',
            likes: 28,
            comments: Array(16).fill({})
        },
        {
            id: 7,
            title: '연말정산 꿀팁 공유',
            content: '세금 환급 최대화하는 방법...',
            author: '세금전문가',
            created_at: '2025-05-13T07:00:00Z',
            likes: 45,
            comments: Array(25).fill({})
        },
        {
            id: 8,
            title: '부동산 투자 실패 사례',
            content: '실패에서 배우는 교훈...',
            author: '부동산전문가',
            created_at: '2025-05-12T06:00:00Z',
            likes: 32,
            comments: Array(18).fill({})
        },
        {
            id: 9,
            title: '저축의 즐거움',
            content: '돈 모으는 재미있는 방법들...',
            author: '머니러버',
            created_at: '2025-05-11T05:00:00Z',
            likes: 19,
            comments: Array(9).fill({})
        },
        {
            id: 10,
            title: '투자 심리 관리하기',
            content: '감정적 투자를 피하는 방법...',
            author: '멘탈케어',
            created_at: '2025-05-10T04:00:00Z',
            likes: 27,
            comments: Array(14).fill({})
        },
        {
            id: 11,
            title: '은행 적금 비교 분석',
            content: '현재 가장 유리한 적금 상품은?',
            author: '금융전문가',
            created_at: '2025-05-09T03:00:00Z',
            likes: 33,
            comments: Array(22).fill({})
        }
    ].sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
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
}

.comment-count {
    color: #145c2b;
    font-size: 0.9rem;
    margin-left: 0.5rem;
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
