<template>
  <div class="user-detail-container">
    <!-- 성향 테스트 결과 카드 -->
    <div class="content-card">
      <div class="card-header">
        <h3>투자 성향 분석</h3>
      </div>
      <div class="card-content">
        <template v-if="user.test_result">
          <div class="test-result">
            <div class="result-header">
              <div class="result-type-text">{{ user.nickname }}님은</div>
              <div class="result-type">{{ user.test_result.type }}</div>
            </div>
            <div class="result-score">총점: {{ user.test_result.total_score }}점</div>
          </div>
        </template>
        <div v-else class="empty-state">
          <i class="fas fa-chart-line"></i>
          <p>아직 투자 성향 테스트를 하지 않으셨네요!</p>
          <p class="sub-text">투자 성향 테스트로 자신의 투자 스타일을 알아보세요.</p>
        </div>
      </div>
    </div>

    <!-- 찜한 상품 카드 -->
    <div class="content-card">
      <div class="card-header">
        <h3>찜한 상품</h3>
        <button v-if="user.liked_products?.length" class="action-button" @click="goToSavings">
          전체보기
        </button>
      </div>
      <div class="card-content">
        <template v-if="user.liked_products?.length">
          <ul class="product-list">
            <li v-for="product in user.liked_products" :key="product.id" class="product-item">
              <div class="product-info-header">
                <span class="product-type">{{ product.type === 'deposit' ? '정기예금' : '적금' }}</span>
                <span class="bank-name">{{ product.company }}</span>
              </div>
              <div class="product-name">{{ product.name }}</div>
              <div class="product-details">
                <div class="rate-info">
                  <span class="label">금리</span>
                  <span class="value">{{ product.interest_rate }}% ~ {{ product.special_rate }}%</span>
                </div>
                <div class="term-info">
                  <span class="label">기간</span>
                  <span class="value">{{ product.term }}개월</span>
                </div>
              </div>
            </li>
          </ul>
        </template>
        <div v-else class="empty-state">
          <i class="fas fa-heart"></i>
          <p>아직 찜한 상품이 없습니다.</p>
          <p class="sub-text">{{ user.nickname }}님이 아직 찜한 상품이 없습니다.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const goToSavings = () => {
  router.push({ name: 'savings' })
}
</script>

<style scoped>
.user-detail-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.content-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

.action-button {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: 1px solid #dee2e6;
  background: white;
  color: #495057;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.action-button:hover {
  background: #e9ecef;
}

.card-content {
  padding: 1.5rem;
}

.product-info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.product-type {
  font-size: 0.8rem;
  padding: 0.2rem 0.5rem;
  background-color: #e3f2fd;
  color: #1976d2;
  border-radius: 4px;
}

.bank-name {
  font-size: 0.9rem;
  color: #666;
}

.product-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.product-details {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
}

.rate-info, .term-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.label {
  color: #666;
}

.value {
  font-weight: 500;
  color: #333;
}

.rate-info .value {
  color: #e64545;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.empty-state i {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #145c2b;
}

.empty-state p {
  margin: 0.5rem 0;
  font-size: 1.1rem;
  color: #333;
}

.empty-state .sub-text {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 1.5rem;
}

.product-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.product-item {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.product-item:last-child {
  border-bottom: none;
}

.test-result {
  text-align: center;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.result-header {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.result-type-text {
  font-size: 1.2rem;
  color: #495057;
}

.result-type {
  font-size: 1.5rem;
  font-weight: 700;
  color: #145c2b;
}

.result-score {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 1rem;
}
</style> 