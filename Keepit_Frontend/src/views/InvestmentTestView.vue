<template>
  <div class="test-container">
    <h1 class="test-title">투자 성향 테스트</h1>
    
    <div v-if="!isSubmitted" class="test-form">
      <div v-for="(question, index) in questions" :key="index" class="question-box">
        <h3>Q{{ index + 1 }}. {{ question.text }}</h3>
        <div class="options">
          <label v-for="(option, optIndex) in question.options" :key="optIndex" class="option-label">
            <input 
              type="radio" 
              :name="'q' + (index + 1)"
              :value="optIndex + 1"
              v-model="answers[index]"
              required
            >
            {{ option }}
          </label>
        </div>
      </div>

      <button 
        class="submit-btn" 
        @click="submitTest"
        :disabled="!isAllAnswered"
      >
        테스트 제출하기
      </button>
    </div>

    <div v-else class="loading">
      결과를 분석중입니다...
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/users.js'
import axios from 'axios'

const accountStore = useAccountStore()
const router = useRouter()
const isSubmitted = ref(false)
const answers = ref(Array(6).fill(null))

const questions = [
  {
    text: '당신의 나이는?',
    options: ['20대 이하', '30~40대', '50대 이상']
  },
  {
    text: '당신의 투자 경험은 어느 정도인가요?',
    options: ['없음', '약간 있음', '매우 많음']
  },
  {
    text: '투자 손실이 발생했을 때 당신의 반응은?',
    options: ['전부 인출', '일부 유지', '추가 매수']
  },
  {
    text: '당신의 주 수입원은?',
    options: ['불안정 (자영업, 아르바이트 등)', '보통 (정규직 등)', '매우 안정 (공무원, 연금 등)']
  },
  {
    text: '투자 시 기대 수익률은?',
    options: ['3% 이하', '5~8%', '10% 이상']
  },
  {
    text: '갑작스러운 큰 지출이 생기면 어떻게 대응할 수 있나요?',
    options: ['전혀 대비 안 됨', '일부 대비됨', '충분히 대비됨']
  }
]

const isAllAnswered = computed(() => {
  return answers.value.every(answer => answer !== null)
})

const submitTest = async () => {
  if (!isAllAnswered.value) {
    alert('모든 문항에 답해주세요.')
    return
  }

  if (!accountStore.isAuthenticated || !accountStore.token) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'login', query: { redirect: '/test' } })
    return
  }

  console.log('토큰 확인:', accountStore.token)
  console.log('로그인 상태:', accountStore.isAuthenticated)

  isSubmitted.value = true

  try {
    const formattedAnswers = {
      q1_age: answers.value[0],
      q2_experience: answers.value[1],
      q3_loss_response: answers.value[2],
      q4_income: answers.value[3],
      q5_expected_return: answers.value[4],
      q6_emergency: answers.value[5]
    }

    console.log('제출할 데이터:', formattedAnswers)

    const response = await axios.post('http://127.0.0.1:8000/api/v1/test/submit/', 
      formattedAnswers,
      {
        headers: {
          Authorization: `Token ${accountStore.token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    console.log('테스트 제출 성공:', response.data)
    
    const resultResponse = await axios.get('http://127.0.0.1:8000/api/v1/test/result/', {
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
    
    console.log('테스트 결과 데이터:', resultResponse.data)
    router.push({ 
      name: 'testresult',
      state: { testResult: resultResponse.data }
    })
  } catch (err) {
    console.error('테스트 제출 실패:', err.response?.data || err)
    if (err.response?.status === 401) {
      accountStore.logOut()
      alert('로그인이 만료되었습니다. 다시 로그인해주세요.')
      router.push({ name: 'login', query: { redirect: '/test' } })
    } else {
      alert('테스트 제출에 실패했습니다. 다시 시도해주세요.')
    }
    isSubmitted.value = false
  }
}
</script>

<style scoped>
.test-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.test-title {
  text-align: center;
  color: #145c2b;
  margin-bottom: 2rem;
}

.question-box {
  background: white;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.question-box h3 {
  color: #333;
  margin-bottom: 1rem;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.option-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.option-label:hover {
  background-color: #f5f5f5;
}

.submit-btn {
  display: block;
  width: 100%;
  max-width: 300px;
  margin: 2rem auto;
  padding: 1rem;
  background-color: #145c2b;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.submit-btn:not(:disabled):hover {
  background-color: #0d4420;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #666;
}
</style> 