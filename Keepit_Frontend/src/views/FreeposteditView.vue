<template>
    <div class="edit-page">
        <router-link :to="{ name: 'freecommunity' }" class="back-link">&gt; 자유 게시판</router-link>
        <h2>게시글 수정</h2>
        <form @submit.prevent="submitEdit" class="edit-form">
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
                <button type="submit" class="btn-submit">수정 완료</button>
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/users'

const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()
const postId = route.params.id

const title = ref('')
const content = ref('')

onMounted(async () => {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/v1/community/free/${postId}/`, {
            headers: {
                Authorization: `Token ${accountStore.token}`
            }
        })
        
        // 작성자 확인
        if (response.data.author_id !== accountStore.userId) {
            alert('자신의 게시글만 수정할 수 있습니다.')
            router.push({ name: 'freepostdetail', params: { id: postId } })
            return
        }
        
        title.value = response.data.title
        content.value = response.data.content
    } catch (err) {
        console.error('게시글 조회 실패:', err)
        if (err.response?.status === 401) {
            alert('로그인이 필요합니다.')
            router.push({ name: 'login' })
        } else {
            alert('게시글을 불러오는데 실패했습니다.')
            router.push({ name: 'freecommunity' })
        }
    }
})

const submitEdit = async () => {
    if (!title.value.trim() || !content.value.trim()) {
        alert('제목과 내용을 모두 입력하세요.')
        return
    }

    try {
        await axios.put(
            `http://127.0.0.1:8000/api/v1/community/free/${postId}/`,
            {
                title: title.value,
                content: content.value
            },
            {
                headers: {
                    Authorization: `Token ${accountStore.token}`,
                    'Content-Type': 'application/json'
                }
            }
        )
        alert('게시글이 수정되었습니다.')
        router.push({ name: 'freepostdetail', params: { id: postId } })
    } catch (err) {
        console.error('게시글 수정 실패:', err)
        if (err.response?.status === 401) {
            alert('로그인이 필요합니다.')
            router.push({ name: 'login' })
        } else if (err.response?.status === 403) {
            alert('자신의 게시글만 수정할 수 있습니다.')
            router.push({ name: 'freepostdetail', params: { id: postId } })
        } else {
            alert('게시글 수정 중 오류가 발생했습니다.')
        }
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
