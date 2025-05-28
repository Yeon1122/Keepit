<template>
  <div class="investment-test">
    <div class="test-container">
      <div class="test-header">
        <h1 class="test-title">투자 성향 테스트</h1>
        <p class="test-description">
          아래 문항들에 답변해주시면 고객님께 맞는 투자 상품을 추천해드립니다.
        </p>
      </div>

      <form @submit.prevent="submitTest" class="test-form">
        <div v-for="question in questions" :key="question.id" class="question-item">
          <label :for="question.id" class="question-label">
            {{ question.question }}
          </label>

          <!-- 숫자 입력 필드 -->
          <input
            v-if="question.type === 'number'"
            :id="question.id"
            v-model.number="answers[question.id]"
            type="number"
            :placeholder="question.placeholder"
            class="input-field"
            required
          />

          <!-- 선택 필드 -->
          <select
            v-if="question.type === 'select'"
            :id="question.id"
            v-model="answers[question.id]"
            class="select-field"
            required
          >
            <option value="" disabled selected>선택해주세요</option>
            <option
              v-for="choice in question.choices"
              :key="choice.value"
              :value="choice.value"
            >
              {{ choice.text }}
            </option>
          </select>
        </div>

        <button type="submit" class="submit-button">
          테스트 결과 확인하기
          <i class="fas fa-arrow-right"></i>
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/users.js'

export default {
  name: 'InvestmentTestView',
  
  setup() {
    const router = useRouter()
    const accountStore = useAccountStore()
    const questions = ref([])
    const answers = ref({})

    onMounted(async () => {
      const token = accountStore.token
      if (!token) {
        alert('로그인이 필요한 서비스입니다.')
        router.push({ name: 'login' })
        return
      }

      // 기존 테스트 결과 확인
      try {
        const response = await axios.get('/api/v1/test/result/', {
          headers: {
            Authorization: `Token ${token}`
          }
        })
        
        if (response.data) {
          const confirmed = confirm('이미 투자 성향 테스트 결과가 있습니다. 정말 다시 하시겠습니까?')
          if (!confirmed) {
            router.push({ name: 'testresult' })
            return
          }
        }
      } catch (err) {
        // 결과가 없는 경우(404) 또는 다른 에러는 무시하고 테스트 진행
        console.log('기존 테스트 결과 없음:', err)
      }

      // 테스트 문항 가져오기
      try {
        const response = await axios.get('/api/v1/test/', {
          headers: {
            Authorization: `Token ${token}`
          }
        })
        questions.value = response.data.questions
      } catch (err) {
        console.error('테스트 문항 로딩 실패:', err)
        alert('테스트 문항을 불러오는데 실패했습니다.')
      }
    })

    const submitTest = async () => {
      const token = accountStore.token
      try {
        await axios.post('/api/v1/test/submit/', answers.value, {
          headers: {
            Authorization: `Token ${token}`
          }
        })
        router.push({ name: 'testresult' })
      } catch (error) {
        console.error('테스트 제출 실패:', error)
        alert('테스트 제출에 실패했습니다.')
      }
    }

    return {
      questions,
      answers,
      submitTest
    }
  }
}
</script>

<style scoped>
.investment-test {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.test-container {
  background-color: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.test-header {
  text-align: center;
  margin-bottom: 3rem;
}

.test-title {
  font-size: 2.5rem;
  color: #145c2b;
  margin-bottom: 1rem;
  font-weight: 700;
}

.test-description {
  color: #666;
  font-size: 1.1rem;
  line-height: 1.6;
}

.question-item {
  background-color: #f8f9fa;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  transition: transform 0.2s ease;
}

.question-item:hover {
  transform: translateY(-2px);
}

.question-label {
  display: block;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #333;
  font-weight: 600;
}

.input-field,
.select-field {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1.1rem;
  background-color: white;
  transition: all 0.2s ease;
  color: #333;
}

.input-field:focus,
.select-field:focus {
  outline: none;
  border-color: #145c2b;
  box-shadow: 0 0 0 3px rgba(20, 92, 43, 0.1);
}

/* 드롭다운 옵션 스타일링 */
.select-field option {
  font-size: 1.1rem;
  padding: 1rem;
  background-color: white;
}

/* 드롭다운 호버 효과 */
.select-field option:hover,
.select-field option:focus {
  background-color: rgba(20, 92, 43, 0.1) !important;
  color: #145c2b;
}

/* 선택된 옵션 스타일링 */
.select-field option:checked {
  background-color: #145c2b;
  color: white;
}

.submit-button {
  background-color: #145c2b;
  color: white;
  padding: 1.2rem 2.5rem;
  border: none;
  border-radius: 12px;
  font-size: 1.2rem;
  font-weight: 600;
  cursor: pointer;
  width: 100%;
  margin-top: 2rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.submit-button:hover {
  background-color: #0d4420;
  transform: translateY(-2px);
}

.submit-button i {
  transition: transform 0.3s ease;
}

.submit-button:hover i {
  transform: translateX(5px);
}

@media (max-width: 768px) {
  .investment-test {
    padding: 1rem;
  }

  .test-container {
    padding: 1.5rem;
  }

  .test-title {
    font-size: 2rem;
  }

  .question-item {
    padding: 1.5rem;
  }

  .question-label {
    font-size: 1.1rem;
  }
}
</style>
