<template>
    <form @submit.prevent="onSignUp">
        <label>이름: </label>
        <input type="text" v-model="form.name" />
        <br>
        <label>아이디: </label>
        <input type="text" v-model="form.userid" />
        <br>
        <label>닉네임: </label>
        <input type="text" v-model="form.nickname" />
        <br>
        <label>이메일: </label>
        <input type="email" v-model="form.email" />
        <br>
        <label>비밀번호: </label>
        <input type="password" v-model="form.password" />
        <br>
        <label>비밀번호 확인: </label>
        <input type="password" v-model="form.confirmPassword" />
        <br>
        <label>생년월일:</label>
        <div class="birth-select">
            <select v-model="form.birthYear">
                <option disabled value="">년</option>
                <option v-for="year in birthYears" :key="year" :value="year">{{ year }}</option>
            </select>
            <select v-model="form.birthMonth">
                <option disabled value="">월</option>
                <option v-for="month in birthMonths" :key="month" :value="month">{{ month }}</option>
            </select>
            <select v-model="form.birthDay">
                <option disabled value="">일</option>
                <option v-for="day in birthDays" :key="day" :value="day">{{ day }}</option>
            </select>
        </div>
        <br>
        <label>소득 범위</label>
        <select v-model="form.incomeRange">
            <option disabled value="">선택하세요</option>
            <option>2000만원 이하</option>
            <option>2000만원~4000만원</option>
            <option>4000만원~6000만원</option>
            <option>6000만원 이상</option>
        </select>
        <br>
        <label>지역(시/도)</label>
        <select v-model="form.regionCity" @change="updateDistricts">
            <option disabled value="">선택하세요</option>
            <option v-for="region in mapInfo" :key="region.name" :value="region.name">
                {{ region.name }}
            </option>
        </select>
        <br>
        <label>지역(시/구/군)</label>
        <select v-model="form.regionDistrict" :disabled="!form.regionCity">
            <option disabled value="">선택하세요</option>
            <option v-for="district in filteredDistricts" :key="district" :value="district">
                {{ district }}
            </option>
        </select>
        <br>
        <button type="submit">회원가입</button>
    </form>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts.js'
import mapData from '@/assets/data/mapInfo.json'
import birthData from '@/assets/data/birthDropdown.json'

const accountStore = useAccountStore()

// 사용자 입력값 상태
const form = ref({
    name: '',
    userid: '',
    nickname: '',
    email: '',
    password: '',
    confirmPassword: '',
    birthYear: '',
    birthMonth: '',
    birthDay: '',
    incomeRange: '',
    regionCity: '',
    regionDistrict: '',
})

// 생년월일 데이터
const birthYears = ref(birthData.years)
const birthMonths = ref(birthData.months)
const birthDays = ref(birthData.days)

// 지역 정보 로드
const mapInfo = ref(mapData.mapInfo)

const filteredDistricts = computed(() => {
    const selected = mapInfo.value.find(region => region.name === form.value.regionCity)
    return selected ? selected.countries : []
})

const updateDistricts = () => {
    form.value.regionDistrict = ''
}

// 유효성 검사
const validateForm = () => {
    if (!form.value.userid || !form.value.password) {
        alert('아이디와 비밀번호는 필수입니다!')
        return false
    }
    if (form.value.password.length < 6) {
        alert('비밀번호는 6자 이상이어야 합니다.')
        return false
    }
    if (form.value.password !== form.value.confirmPassword) {
        alert('비밀번호와 비밀번호 확인이 일치하지 않습니다!')
        return false
    }
    if (!form.value.regionCity || !form.value.regionDistrict) {
        alert('지역을 선택하세요!')
        return false
    }
    return true
}

// 회원가입 함수
const onSignUp = () => {
    if (!validateForm()) return

    const requestData = { ...form.value }
    console.log('회원가입 요청 데이터:', requestData)
    // accountStore.signUp({ ...form.value })
}
</script>

<style scoped>
form {
    background-color: white;
    color: black;
    padding: 2rem;
    border-radius: 8px;
    width: 100%;
    max-width: 400px;
    margin: auto;
    font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

label {
    display: block;
    margin: 1rem 0 0.25rem;
    font-weight: 600;
}

input,
select {
    width: 100%;
    padding: 0.6rem 0.8rem;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 0.95rem;
    background-color: #f9f9f9;
    box-sizing: border-box;
}

.birth-select {
    display: flex;
    gap: 0.5rem;
}

.birth-select select {
    flex: 1;
}

button[type="submit"] {
    margin-top: 2rem;
    width: 100%;
    background-color: #145c2b;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 6px;
    padding: 0.9rem;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

button[type="submit"]:hover {
    background-color: #0e4a21;
}
</style>
