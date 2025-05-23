<template>
    <div class="compare-container">
        <!-- 왼쪽: 선택 영역 -->
        <div class="left-panel">
            <!-- 예금/적금 선택 -->
            <div class="filter-bar">
                <div class="btn-group">
                    <button :class="{ active: selectedType === 'deposit' }" @click="changeType('deposit')">정기예금</button>
                    <button :class="{ active: selectedType === 'saving' }" @click="changeType('saving')">적금</button>
                </div>
            </div>

            <!-- 찜한 상품 목록 -->
            <div class="favorites-list">
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
                <table>
                    <thead>
                        <tr>
                            <th>항목</th>
                            <th>{{ comparisonResult[0].company }}<br />{{ comparisonResult[0].name }}</th>
                            <th>{{ comparisonResult[1].company }}<br />{{ comparisonResult[1].name }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>기본 금리</td>
                            <td>{{ comparisonResult[0].interest_rate }}%</td>
                            <td>{{ comparisonResult[1].interest_rate }}%</td>
                        </tr>
                        <tr>
                            <td>기간</td>
                            <td>{{ comparisonResult[0].term }}개월</td>
                            <td>{{ comparisonResult[1].term }}개월</td>
                        </tr>
                        <tr>
                            <td>예상 수령액</td>
                            <td>{{ formatNumber(comparisonResult[0].expected_amount) }}원</td>
                            <td>{{ formatNumber(comparisonResult[1].expected_amount) }}원</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import SavingCard from '@/components/SavingCard.vue'

const route = useRoute()
const selectedType = ref(route.query.type === 'saving' ? 'saving' : 'deposit')
const favorites = ref([])
const selectedProducts = ref([])

const depositAmount = ref(1000000)
const savingMonthlyAmount = ref(100000)
const selectedTerm = ref(12)

const comparisonResult = ref([])

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

    comparisonResult.value = selectedProducts.value.map(product => ({
        ...product,
        term: selectedTerm.value,
        expected_amount: (selectedType.value === 'saving'
            ? savingMonthlyAmount.value * selectedTerm.value * (1 + product.interest_rate / 100)
            : depositAmount.value * (1 + product.interest_rate / 100))
    }))
}

const formatNumber = (val) => val?.toLocaleString() || '-'

onMounted(() => {
    favorites.value = [
        { type: 'deposit', name: '플러스 예금', company: '우리은행', interest_rate: 2.5, special_rate: 2.7 },
        { type: 'deposit', name: '스마트 예금', company: '국민은행', interest_rate: 2.3, special_rate: 2.6 },
        { type: 'saving', name: '하나 적금', company: '하나은행', interest_rate: 3.2, special_rate: 3.5 },
        { type: 'saving', name: '더드림 적금', company: '신한은행', interest_rate: 3.0, special_rate: 3.3 }
    ]
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
    margin-top: 24px;
}

.comparison-table table {
    width: 100%;
    border-collapse: collapse;
}

.comparison-table th,
.comparison-table td {
    border: 1px solid #ccc;
    padding: 8px;
    text-align: center;
}
</style>
