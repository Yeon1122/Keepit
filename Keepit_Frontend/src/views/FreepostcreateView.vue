<template>
    <div class="post-create">
        <router-link :to="{ name: 'freecommunity' }" class="back-link">&gt; 자유 게시판</router-link>
        <h2>자유 글쓰기</h2>
        <form @submit.prevent="submitPost">
            <div class="form-group">
                <label for="title">제목</label>
                <input id="title" v-model="title" type="text" placeholder="제목을 입력하세요" required />
            </div>

            <div class="form-group">
                <label for="content">내용</label>
                <textarea id="content" v-model="content" rows="12" placeholder="내용을 입력하세요" required></textarea>
            </div>

            <div class="button-group">
                <button type="button" class="btn-cancel" @click="$router.go(-1)">취소</button>
                <button type="submit" class="btn-submit">작성 완료</button>
            </div>
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

form {
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
    min-height: 200px;
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
