<template>
    <div class="post-list">
        <div class="header-bar">
            <h2>자유 게시판</h2>
            <router-link :to="{ name: 'freepostcreate' }">
                <button class="write-btn">글쓰기</button>
            </router-link>
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
// import axios from 'axios'

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
            title: 'Vue로 만든 게시판',
            content: '이건 테스트용 게시글이에요',
            created_at: '2025-05-18T14:00:00Z',
            author: '홍길동',
            likes: 2,
            comments: [{}]
        },
        {
            id: 2,
            title: '하이',
            content: '본문입니다',
            created_at: '2025-05-19T09:00:00Z',
            author: '하연',
            likes: 5,
            comments: [{}, {}, {}, {}, {}]
        },
        {
            id: 3,
            title: '세 번째 글',
            author: '민수',
            created_at: '2025-05-17T10:30:00Z',
            likes: 3,
            comments: []
        },
        {
            id: 4,
            title: '네 번째 글',
            author: '지우',
            created_at: '2025-05-16T12:00:00Z',
            likes: 1,
            comments: [{}]
        },
        {
            id: 5,
            title: '다섯 번째',
            author: '유진',
            created_at: '2025-05-15T09:00:00Z',
            likes: 0,
            comments: []
        },
        {
            id: 6,
            title: '여섯 번째 글',
            author: '하람',
            created_at: '2025-05-14T08:00:00Z',
            likes: 4,
            comments: [{}]
        },
        {
            id: 7,
            title: '일곱 번째',
            author: '가영',
            created_at: '2025-05-13T07:00:00Z',
            likes: 2,
            comments: []
        },
        {
            id: 8,
            title: '여덟 번째',
            author: '지후',
            created_at: '2025-05-12T06:00:00Z',
            likes: 1,
            comments: [{}]
        },
        {
            id: 9,
            title: '아홉 번째',
            author: '하진',
            created_at: '2025-05-11T05:00:00Z',
            likes: 2,
            comments: []
        },
        {
            id: 10,
            title: '열 번째',
            author: '도윤',
            created_at: '2025-05-10T04:00:00Z',
            likes: 3,
            comments: [{}]
        },
        {
            id: 11,
            title: '열한 번째',
            author: '서준',
            created_at: '2025-05-09T03:00:00Z',
            likes: 1,
            comments: []
        }
    ].sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
})
</script>

<style scoped>
.post-list {
    max-width: 900px;
    margin: 0 auto;
    padding: 1rem;
    font-family: 'Pretendard', sans-serif;
}

/* ✅ 상단 바 */
.header-bar {
    background-color: #145c2b;
    color: white;
    padding: 1rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 1rem 1rem 0 0;
}

.write-btn {
    background: white;
    color: #145c2b;
    padding: 0.4rem 1.2rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    border: 2px solid white;
}

.write-btn:hover {
    background-color: #f2f2f2;
}

/* ✅ 카드 스타일 */
.post-card {
    background: white;
    margin-top: 0.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    padding: 1rem 1.5rem;
}

.post-link {
    text-decoration: none;
    color: inherit;
    display: block;
}

.card-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.no {
    width: 40px;
    text-align: left;
    font-weight: 200;
    color: #888;
}

.title {
    flex-grow: 1;
    font-weight: bold;
}

.comment-count {
    margin-left: 0.4rem;
    color: #145c2b;
    font-weight: normal;
}

.author,
.date {
    width: 100px;
    text-align: center;
    font-size: 0.9rem;
    color: #555;
}

.no-posts {
    text-align: center;
    margin-top: 2rem;
    color: #888;
}

.pagination {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 1.5rem;
}

.pagination button {
    padding: 0.4rem 0.8rem;
    border: 1px solid #ccc;
    background-color: white;
    color: #145c2b;
    font-weight: bold;
    border-radius: 4px;
    cursor: pointer;
}

.pagination button.active {
    background-color: #145c2b;
    color: white;
    border-color: #145c2b;
}
</style>
