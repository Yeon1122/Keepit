<template>
    <div class="post-create">
        <h2>자유 글쓰기</h2>
        <form @submit.prevent="submitPost">
            <label>제목</label>
            <input v-model="title" type="text" required />

            <label>내용</label>
            <textarea v-model="content" rows="8" required></textarea>

            <button type="submit">작성 완료</button>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
// import axios from 'axios' // ✅ 실제 백엔드 연동 시 주석 해제

const router = useRouter()
const category = 'free'

const title = ref('')
const content = ref('')

const submitPost = async () => {
    const payload = {
        title: title.value,
        content: content.value
    }

    // ✅ 백엔드에 전송할 때 사용
    // try {
    //   await axios.post(`http://127.0.0.1:8000/api/v1/posts/free/`, payload)
    //   router.push({ name: 'freecommunity' })
    // } catch (err) {
    //   console.error('❌ 글 작성 실패:', err)
    //   alert('글 작성 중 오류가 발생했습니다.')
    // }

    console.log('📝 더미 작성 완료:', payload)
    alert('작성 완료! (더미)')
    router.push({ name: 'freecommunity' })
}
</script>

<style scoped>
.post-create {
    max-width: 720px;
    margin: 0 auto;
    padding: 1rem;
}

form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

input,
textarea {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
}

button {
    background: #145c2b;
    color: white;
    padding: 0.6rem 1.5rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
</style>
