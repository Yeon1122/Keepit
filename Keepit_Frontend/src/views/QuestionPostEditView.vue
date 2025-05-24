<template>
    <div class="edit-page">
        <router-link :to="{ name: 'questioncommunity' }" class="back-link">&gt; 질문 게시판</router-link>
        <h2>질문 수정</h2>
        <form @submit.prevent="submitEdit" class="edit-form">
            <div class="form-group">
                <label for="title">제목</label>
                <input id="title" v-model="title" type="text" placeholder="질문의 제목을 입력하세요" required />
            </div>

            <div class="form-group">
                <label for="content">내용</label>
                <textarea id="content" v-model="content" rows="12" placeholder="질문 내용을 자세히 입력하세요" required></textarea>
            </div>

            <div class="button-group">
                <button type="button" class="btn-cancel" @click="$router.go(-1)">취소</button>
                <button type="submit" class="btn-submit">수정 완료</button>
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const postId = route.params.id

const title = ref('')
const content = ref('')

onMounted(async () => {
    try {
        // const res = await axios.get(`/api/v1/posts/question/${postId}/`)
        // title.value = res.data.title
        // content.value = res.data.content

        // 더미 데이터
        if (postId === '1') {
            title.value = '주식투자 초보자인데 ETF 추천해주세요'
            content.value = '안정적인 ETF 위주로 추천 부탁드립니다. 월 100만원 정도 투자할 예정입니다.'
        } else {
            title.value = '기존 질문 제목'
            content.value = '기존 질문 내용입니다.'
        }
    } catch (err) {
        console.error('질문 조회 실패:', err)
    }
})

const submitEdit = async () => {
    if (!title.value.trim() || !content.value.trim()) {
        alert('제목과 내용을 모두 입력하세요.')
        return
    }

    try {
        // await axios.put(`/api/v1/posts/question/${postId}/`, {
        //     title: title.value,
        //     content: content.value
        // })

        alert('질문이 수정되었습니다.')
        router.push({ name: 'questiondetail', params: { id: postId } })
    } catch (err) {
        console.error('질문 수정 실패:', err)
        alert('질문 수정 중 오류가 발생했습니다.')
    }
}
</script>

<style scoped>
.edit-page {
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

h2 {
    font-size: 1.5rem;
    color: #1a1a1a;
    margin: 1.5rem 0;
    font-weight: 600;
}

.edit-form {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
    border: 1px solid #e0e0e0;
}

.form-group {
    margin-bottom: 1.5rem;
}

label {
    display: block;
    font-size: 1rem;
    color: #1a1a1a;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

input,
textarea {
    width: 100%;
    padding: 0.8rem 1rem;
    font-size: 1rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    background: #fff;
    transition: all 0.2s ease;
}

input:focus,
textarea:focus {
    outline: none;
    border-color: #145c2b;
    box-shadow: 0 0 0 3px rgba(20, 92, 43, 0.1);
}

textarea {
    resize: vertical;
    min-height: 300px;
    line-height: 1.6;
}

.button-group {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 2rem;
}

.btn-cancel {
    padding: 0.8rem 1.5rem;
    border: 1px solid #e0e0e0;
    background: white;
    color: #666;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.95rem;
    transition: all 0.2s ease;
}

.btn-cancel:hover {
    border-color: #145c2b;
    color: #145c2b;
}

.btn-submit {
    padding: 0.8rem 1.5rem;
    background: #145c2b;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 500;
    transition: all 0.2s ease;
}

.btn-submit:hover {
    background: #0d3d1d;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(20, 92, 43, 0.2);
}
</style> 