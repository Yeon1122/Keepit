<template>
    <div class="edit-page">
        <h2>게시글 수정</h2>
        <form @submit.prevent="submitEdit" class="edit-form">
            <label for="title">제목</label>
            <input id="title" v-model="title" placeholder="제목을 입력하세요" />

            <label for="content">내용</label>
            <textarea id="content" v-model="content" placeholder="내용을 입력하세요"></textarea>

            <button type="submit" class="btn-green">수정 완료</button>
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
    // const res = await axios.get(`http://localhost:8000/api/v1/posts/free/${postId}/`)
    // title.value = res.data.title
    // content.value = res.data.content

    // 더미 데이터
    title.value = '기존 제목'
    content.value = '기존 내용'
})

const submitEdit = async () => {
    if (!title.value.trim() || !content.value.trim()) {
        alert('제목과 내용을 모두 입력하세요.')
        return
    }

    // await axios.put(`http://localhost:8000/api/v1/posts/free/${postId}/`, {
    //   title: title.value,
    //   content: content.value
    // })

    alert('게시글이 수정되었습니다.')
    router.push({ name: 'freepostdetail', params: { id: postId } })
}
</script>

<style scoped>
.edit-page {
    max-width: 720px;
    margin: 0 auto;
    padding: 2rem 1rem;
}

.edit-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

input,
textarea {
    width: 100%;
    padding: 0.6rem;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 6px;
}

textarea {
    height: 200px;
    resize: vertical;
}

.btn-green {
    background-color: #145c2b;
    color: white;
    border: none;
    padding: 0.6rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
    align-self: flex-start;
}
</style>
