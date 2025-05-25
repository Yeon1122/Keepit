<template>
    <div class="compare-container">
        <!-- 로딩 상태 -->
        <div v-if="loading" class="loading-state">
            데이터를 불러오는 중입니다...
        </div>

        <!-- 에러 상태 -->
        <div v-else-if="error" class="error-state">
            {{ error }}
            <button @click="fetchFavorites" class="retry-button">다시 시도</button>
        </div>

        <!-- 데이터 표시 -->
        <template v-else>
            <!-- 왼쪽: 선택 영역 -->
            <div class="left-panel">
                <!-- 예금/적금 선택 -->
                <div class="filter-bar">
                    <div class="btn-group">
                        <button :class="{ active: selectedType === 'deposit' }" @click="changeType('deposit')">정기예금</button>
                        <button :class="{ active: selectedType === 'saving' }" @click="changeType('saving')">적금</button>
                    </div>
                </div>

                <!-- 찜한 상품이 없을 때 메시지 -->
                <div v-if="filteredFavorites.length === 0" class="no-favorites">
                    <p>찜한 {{ selectedType === 'deposit' ? '정기예금' : '적금' }} 상품이 없습니다.</p>
                    <p>상품을 둘러보고 마음에 드는 상품을 찜해보세요!</p>
                    <router-link 
                        :to="{ name: selectedType === 'deposit' ? 'deposits' : 'savings' }" 
                        class="browse-button"
                    >
                        {{ selectedType === 'deposit' ? '정기예금' : '적금' }} 상품 둘러보기
                    </router-link>
                </div>

                <!-- 찜한 상품 목록 -->
                <div v-else class="favorites-list">
                    <div v-for="product in filteredFavorites" :key="product.name + product.company" class="favorite-item">
                        <input class="custom-checkbox" type="checkbox" :value="product" v-model="selectedProducts"
                            :disabled="selectedProducts.length >= 2 && !isSelected(product)" />
                        <SavingCard :product="product" />
                    </div>
                </div>
            </div>

            <!-- 오른쪽: 계산기 + 비교 테이블 -->
            <div class="right-panel">
                <div class="calculator">
                    <div v-if="selectedType === 'deposit'">
                        <label>총 저축 금액 (원)</label>
                        <input type="number" v-model.number="depositAmount" />
                    </div>

                    <div v-if="selectedType === 'saving'">
                        <label>월 저축 금액 (원)</label>
                        <input type="number" v-model.number="savingMonthlyAmount" />
                    </div>

                    <div>
                        <label>저축 기간 (개월)</label>
                        <select v-model.number="selectedTerm">
                            <option v-for="m in [1, 3, 6, 12, 24, 36]" :key="m" :value="m">{{ m }}개월</option>
                        </select>
                    </div>

                    <button @click="compareProducts">비교하기</button>
                </div>

                <!-- 비교 테이블 -->
                <div v-if="comparisonResult.length === 2" class="comparison-table">
                    <div class="comparison-card" v-for="product in comparisonResult" :key="product.name">
                        <div class="card-header">
                            <h3>{{ product.company }}</h3>
                            <h4>{{ product.name }}</h4>
                        </div>
                        <div class="card-body">
                            <div class="info-row">
                                <span class="label">기본 금리</span>
                                <span class="value highlight">{{ product.interest_rate }}%</span>
                            </div>
                            <div class="info-row">
                                <span class="label">기간</span>
                                <span class="value">{{ product.term }}개월</span>
                            </div>
                            <div class="info-row total">
                                <span class="label">예상 수령액</span>
                                <span class="value highlight">{{ formatNumber(product.expected_amount) }}원</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/users'
import SavingCard from '@/components/SavingCard.vue'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()
const selectedType = ref(route.query.type === 'saving' ? 'saving' : 'deposit')
const favorites = ref([])
const selectedProducts = ref([])

const depositAmount = ref(1000000)
const savingMonthlyAmount = ref(100000)
const selectedTerm = ref(12)

const comparisonResult = ref([])
const loading = ref(true)
const error = ref(null)

const changeType = (type) => {
    selectedType.value = type
    selectedProducts.value = []
    comparisonResult.value = []
}

const isSelected = (product) => {
    return selectedProducts.value.some(p => p.name === product.name && p.company === product.company)
}

const filteredFavorites = computed(() => {
    return favorites.value.filter(p => p.type === selectedType.value)
})

const compareProducts = async () => {
    if (selectedProducts.value.length !== 2) {
        alert('2개의 상품을 선택해주세요.')
        return
    }

    try {
        const response = await axios.post(
            `/api/v1/products/compare/${selectedType.value}s/`,
            {
                product_names: selectedProducts.value.map(p => p.name),
                monthly_amount: selectedType.value === 'saving' ? savingMonthlyAmount.value : depositAmount.value,
                months: selectedTerm.value
            },
            {
                headers: { Authorization: `Token ${accountStore.token}` }
            }
        )

        comparisonResult.value = response.data.products.map(product => ({
            ...product,
            company: selectedProducts.value.find(p => p.name === product.name)?.company || '',
            expected_amount: product.expected_amount
        }))
    } catch (err) {
        console.error('비교 실패:', err)
        alert('상품 비교에 실패했습니다.')
    }
}

const formatNumber = (val) => val?.toLocaleString() || '-'

const fetchFavorites = async () => {
    loading.value = true
    error.value = null

    try {
        const response = await axios.get('/api/v1/products/favorites/', {
            headers: { Authorization: `Token ${accountStore.token}` }
        })
        favorites.value = response.data
    } catch (err) {
        console.error('찜한 상품 로딩 실패:', err)
        error.value = '찜한 상품을 불러오는데 실패했습니다.'
    } finally {
        loading.value = false
    }
}

onMounted(async () => {
    if (!accountStore.isAuthenticated) {
        alert('로그인이 필요한 서비스입니다.')
        router.push({ name: 'login' })
        return
    }

    await fetchFavorites()
})
</script>

<style scoped>
.compare-container {
    display: flex;
    gap: 32px;
    padding: 32px;
}

.left-panel,
.right-panel {
    flex: 1;
}

.filter-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.btn-group {
    display: flex;
    gap: 1rem;
}

button {
    padding: 0.6rem 1.5rem;
    border: 2px solid #145c2b;
    background-color: white;
    color: #145c2b;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s;
}

button:hover:not(.active) {
    background-color: #145c2b;
    color: white;
}

button.active {
    background-color: #145c2b;
    color: white;
}

.favorite-item {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 24px;
}

.custom-checkbox {
    transform: scale(1.5);
    align-self: center;
}

.calculator input,
.calculator select {
    margin-bottom: 12px;
    width: 100%;
    padding: 4px;
}

.comparison-table {
    display: flex;
    gap: 2rem;
    margin-top: 2rem;
}

.comparison-card {
    flex: 1;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.card-header {
    background: #145c2b;
    color: white;
    padding: 1.5rem;
    text-align: center;
}

.card-header h3 {
    margin: 0;
    font-size: 1.2rem;
    color: white;
}

.card-header h4 {
    margin: 0.5rem 0 0;
    font-size: 1rem;
    font-weight: normal;
    color: white;
}

.card-body {
    padding: 1.5rem;
}

.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.8rem 0;
    border-bottom: 1px solid #eee;
}

.info-row:last-child {
    border-bottom: none;
}

.info-row.total {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 2px solid #145c2b;
    font-weight: bold;
    font-size: 1.1rem;
}

.label {
    color: #666;
    font-size: 0.9rem;
}

.value {
    font-weight: 500;
}

.value.highlight {
    color: #145c2b;
    font-weight: bold;
    font-size: 1.1rem;
}

.total .value.highlight {
    font-size: 1rem;
}

.calculator {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.calculator input,
.calculator select {
    margin-bottom: 1rem;
    width: 100%;
    padding: 0.8rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

.calculator label {
    display: block;
    margin-bottom: 0.5rem;
    color: #333;
    font-weight: 500;
}

.calculator button {
    width: 100%;
    padding: 1rem;
    font-size: 1.1rem;
    margin-top: 1rem;
}

.loading-state,
.error-state {
    text-align: center;
    padding: 2rem;
    color: #666;
}

.error-state {
    color: #dc3545;
}

.retry-button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background-color: #145c2b;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.retry-button:hover {
    background-color: #0d4420;
}

.no-favorites {
    text-align: center;
    padding: 2rem;
    background: #f8f9fa;
    border-radius: 8px;
    margin: 1rem 0;
}

.no-favorites p {
    margin: 0.5rem 0;
    color: #666;
}

.browse-button {
    display: inline-block;
    margin-top: 1rem;
    padding: 0.8rem 1.5rem;
    background-color: #145c2b;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    transition: background-color 0.2s;
}

.browse-button:hover {
    background-color: #0d4420;
}
</style>
