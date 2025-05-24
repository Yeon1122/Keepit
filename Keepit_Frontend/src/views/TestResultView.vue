<template>
  <div class="result-container">
    <div v-if="loading" class="loading">
      결과를 불러오는 중입니다...
    </div>

    <div v-else-if="result" class="result-content">
      <h1 class="result-title">투자 성향 테스트 결과</h1>
      
      <div class="result-box">
        <div class="result-type">
          <h2>{{ result.type }}</h2>
          <div class="score">총점: {{ result.total_score }}점</div>
        </div>

        <div class="result-description">
          <h3>성향 설명</h3>
          <p>{{ result.description }}</p>
        </div>

        <div class="recommendation">
          <h3>추천 투자 방식</h3>
          <ul>
            <li v-for="(item, index) in result.recommendations" :key="index">
              {{ item }}
            </li>
          </ul>
        </div>
      </div>

      <div class="action-buttons">
        <button @click="retakeTest" class="retake-btn">테스트 다시하기</button>
        <button @click="goToMyPage" class="mypage-btn">마이페이지로 이동</button>
      </div>
    </div>

    <div v-else class="error">
      결과를 불러오는데 실패했습니다.
      <button @click="retakeTest" class="retake-btn">테스트 다시하기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const loading = ref(true)
const result = ref(null)

onMounted(async () => {
  const token = sessionStorage.getItem('token')

  if (!token) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'login', query: { redirect: '/test/result' } })
    return
  }

  try {
    const response = await axios.get('http://localhost:8000/api/v1/test/result/', {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    result.value = response.data
  } catch (err) {
    console.error('결과 불러오기 실패:', err)
    if (err.response?.status === 401) {
      alert('로그인이 만료되었습니다. 다시 로그인해주세요.')
      router.push({ name: 'login', query: { redirect: '/test/result' } })
    }
  } finally {
    loading.value = false
  }
})

const getRecommendations = (type) => {
  switch (type) {
    case '안정형':
      return [
        '원금 보장형 상품 위주로 투자',
        '정기예금, 적금 추천',
        '안정적인 채권형 펀드 고려'
      ]
    case '중립형':
      return [
        '적절한 위험-수익 균형 추구',
        '채권형과 주식형 펀드 혼합',
        '안정적인 배당주 투자 고려'
      ]
    case '공격형':
      return [
        '높은 수익을 위한 적극적 투자',
        '주식형 펀드, 해외 투자',
        '신흥 시장 및 섹터 투자 고려'
      ]
    default:
      return []
  }
}

const retakeTest = () => {
  router.push({ name: 'investmenttest' })
}

const goToMyPage = () => {
  router.push({ name: 'mypage' })
}
</script>

<style scoped>
.result-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.result-title {
  text-align: center;
  color: #145c2b;
  margin-bottom: 2rem;
}

.result-box {
  background: white;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.result-type {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #145c2b;
}

.result-type h2 {
  color: #145c2b;
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.score {
  color: #666;
  font-size: 1.1rem;
}

.result-description, .recommendation {
  margin-bottom: 1.5rem;
}

.result-description h3, .recommendation h3 {
  color: #333;
  margin-bottom: 1rem;
}

.recommendation ul {
  list-style: none;
  padding: 0;
}

.recommendation li {
  padding: 0.5rem 0;
  padding-left: 1.5rem;
  position: relative;
}

.recommendation li::before {
  content: "•";
  color: #145c2b;
  position: absolute;
  left: 0;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.retake-btn, .mypage-btn {
  padding: 0.8rem 1.5rem;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.retake-btn {
  background-color: white;
  color: #145c2b;
  border: 2px solid #145c2b;
}

.mypage-btn {
  background-color: #145c2b;
  color: white;
  border: none;
}

.retake-btn:hover {
  background-color: #145c2b;
  color: white;
}

.mypage-btn:hover {
  background-color: #0d4420;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}
</style> 