<template>
  <div class="investment-test">
    <div class="test-container" v-if="!isSubmitted">
      <h1 class="test-title">투자 성향 테스트</h1>
      <p class="test-description">
        아래 문항들에 답변해주시면 고객님께 맞는 투자 상품을 추천해드립니다.
      </p>

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
        </button>
      </form>
    </div>

    <!-- 결과 화면 -->
    <div v-else class="result-container">
      <h2 class="result-title">투자 성향 분석 결과</h2>
      
      <div class="risk-type">
        <h3>투자 성향</h3>
        <p>{{ getRiskTypeDisplay(testResult.risk_type) }}</p>
      </div>

      <div class="recommendations">
        <h3>추천 투자 상품</h3>
        <div class="recommendation-items">
          <div 
            v-for="(isRecommended, type) in testResult.recommendations" 
            :key="type"
            class="recommendation-item"
            :class="{ 'recommended': isRecommended }"
          >
            <span class="product-type">{{ getProductTypeDisplay(type) }}</span>
            <span class="recommendation-status">
              {{ isRecommended ? '추천' : '비추천' }}
            </span>
          </div>
        </div>
      </div>

      <button @click="retakeTest" class="retake-button">
        테스트 다시하기
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'InvestmentTest',
  
  setup() {
    const questions = ref([])
    const answers = ref({})
    const isSubmitted = ref(false)
    const testResult = ref(null)

    // 테스트 문항 로드
    const loadQuestions = async () => {
      try {
        const response = await axios.get('/api/v1/test/')
        questions.value = response.data.questions
      } catch (error) {
        console.error('Failed to load test questions:', error)
      }
    }

    // 테스트 제출
    const submitTest = async () => {
      try {
        const response = await axios.post('/api/v1/test/submit/', answers.value)
        testResult.value = response.data
        isSubmitted.value = true
      } catch (error) {
        console.error('Failed to submit test:', error)
      }
    }

    // 테스트 다시하기
    const retakeTest = () => {
      answers.value = {}
      isSubmitted.value = false
      testResult.value = null
    }

    // 위험 성향 표시
    const getRiskTypeDisplay = (riskType) => {
      const types = {
        conservative: '안정형',
        moderate: '중립형',
        aggressive: '공격형'
      }
      return types[riskType] || riskType
    }

    // 상품 유형 표시
    const getProductTypeDisplay = (type) => {
      const types = {
        deposit: '예금',
        saving: '적금',
        stock: '주식',
        etf: 'ETF',
        goods: '기타 상품'
      }
      return types[type] || type
    }

    onMounted(loadQuestions)

    return {
      questions,
      answers,
      isSubmitted,
      testResult,
      submitTest,
      retakeTest,
      getRiskTypeDisplay,
      getProductTypeDisplay
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

.test-title {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.test-description {
  color: #666;
  margin-bottom: 2rem;
}

.question-item {
  margin-bottom: 2rem;
}

.question-label {
  display: block;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.input-field,
.select-field {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.input-field:focus,
.select-field:focus {
  outline: none;
  border-color: #3498db;
}

.submit-button,
.retake-button {
  background-color: #3498db;
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 4px;
  font-size: 1.1rem;
  cursor: pointer;
  width: 100%;
  margin-top: 2rem;
}

.submit-button:hover,
.retake-button:hover {
  background-color: #2980b9;
}

.result-container {
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
}

.result-title {
  color: #2c3e50;
  margin-bottom: 2rem;
}

.risk-type {
  margin-bottom: 2rem;
}

.risk-type h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.recommendations {
  margin-bottom: 2rem;
}

.recommendations h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.recommendation-items {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.recommendation-item {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: white;
}

.recommendation-item.recommended {
  border-color: #3498db;
  background-color: #ebf5fb;
}

.product-type {
  font-weight: bold;
  color: #2c3e50;
}

.recommendation-status {
  color: #666;
}

.recommendation-item.recommended .recommendation-status {
  color: #3498db;
}
</style> 