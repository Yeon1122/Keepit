<template>
    <div class="signup-container">
        <form @submit.prevent="onSignUp">
            <label>이름: </label>
            <input type="text" :value="form.name" @input="updateField('name', $event.target.value)" />
            
            <label>아이디: </label>
            <div class="input-group">
                <input 
                    type="text" 
                    :value="form.userid"
                    @input="updateField('userid', $event.target.value)"
                    @blur="checkDuplicate('userid')"
                    :class="{ 'error': errors.userid, 'success': validations.userid }"
                />
                <span v-if="errors.userid" class="error-message">{{ errors.userid }}</span>
                <span v-else-if="validations.userid" class="success-message">사용 가능한 아이디입니다.</span>
            </div>
            
            <label>닉네임: </label>
            <div class="input-group">
                <input 
                    type="text" 
                    :value="form.nickname"
                    @input="updateField('nickname', $event.target.value)"
                    @blur="checkDuplicate('nickname')"
                    :class="{ 'error': errors.nickname, 'success': validations.nickname }"
                />
                <span v-if="errors.nickname" class="error-message">{{ errors.nickname }}</span>
                <span v-else-if="validations.nickname" class="success-message">사용 가능한 닉네임입니다.</span>
            </div>
            
            <label>이메일: </label>
            <div class="input-group">
                <input 
                    type="email" 
                    :value="form.email"
                    @input="updateField('email', $event.target.value)"
                    @blur="checkDuplicate('email')"
                    :class="{ 'error': errors.email, 'success': validations.email }"
                />
                <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
                <span v-else-if="validations.email" class="success-message">사용 가능한 이메일입니다.</span>
            </div>
            
            <label>비밀번호: </label>
            <div class="input-group">
                <input 
                    type="password" 
                    :value="form.password"
                    @input="updateField('password', $event.target.value)"
                    :class="{ 'error': errors.password, 'success': validations.password }"
                />
                <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
                <span v-else-if="validations.password" class="success-message">사용 가능한 비밀번호입니다.</span>
            </div>
            
            <label>비밀번호 확인: </label>
            <div class="input-group">
                <input 
                    type="password" 
                    :value="form.confirmPassword"
                    @input="updateField('confirmPassword', $event.target.value)"
                    :class="{ 'error': errors.confirmPassword, 'success': validations.confirmPassword }"
                />
                <span v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</span>
                <span v-else-if="validations.confirmPassword" class="success-message">비밀번호가 일치합니다.</span>
            </div>
            
            <label>생년월일:</label>
            <div class="birth-select">
                <select 
                    v-model="form.birthYear"
                    @change="validateBirthDate"
                    :class="{ 'error': errors.birthDate, 'success': validations.birthDate }">
                    <option disabled value="">년</option>
                    <option v-for="year in birthYears" :key="year" :value="year">{{ year }}</option>
                </select>
                <select 
                    v-model="form.birthMonth"
                    @change="validateBirthDate"
                    :class="{ 'error': errors.birthDate, 'success': validations.birthDate }">
                    <option disabled value="">월</option>
                    <option v-for="month in birthMonths" :key="month" :value="month">{{ month }}</option>
                </select>
                <select 
                    v-model="form.birthDay"
                    @change="validateBirthDate"
                    :class="{ 'error': errors.birthDate, 'success': validations.birthDate }">
                    <option disabled value="">일</option>
                    <option v-for="day in birthDays" :key="day" :value="day">{{ day }}</option>
                </select>
            </div>
            <span v-if="errors.birthDate" class="error-message">{{ errors.birthDate }}</span>
            <span v-else-if="validations.birthDate" class="success-message">올바른 생년월일입니다.</span>
            
            <label>지역(시/도)</label>
            <select v-model="form.regionCity" @change="updateDistricts">
                <option disabled value="">선택하세요</option>
                <option v-for="region in mapInfo" :key="region.name" :value="region.name">
                    {{ region.name }}
                </option>
            </select>
            
            <label>지역(시/구/군)</label>
            <select v-model="form.regionDistrict" :disabled="!form.regionCity">
                <option disabled value="">선택하세요</option>
                <option v-for="district in filteredDistricts" :key="district" :value="district">
                    {{ district }}
                </option>
            </select>
            
            <button type="submit">회원가입</button>
        </form>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAccountStore } from '@/stores/users.js'
import mapData from '@/assets/data/mapInfo.json'
import birthData from '@/assets/data/birthDropdown.json'
import axios from 'axios'

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
    regionCity: '',
    regionDistrict: '',
})

// 에러 메시지 상태
const errors = ref({
    userid: '',
    nickname: '',
    email: '',
    password: '',
    confirmPassword: '',
    birthDate: ''
})

// 유효성 검증 상태
const validations = ref({
    userid: false,
    nickname: false,
    email: false,
    password: false,
    confirmPassword: false,
    birthDate: false
})

// 생년월일 데이터
const birthYears = ref(birthData.years.slice().reverse())
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

// 윤년 체크 함수
const isLeapYear = (year) => {
    return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0)
}

// 날짜 유효성 검사 함수
const isValidDate = (year, month, day) => {
    // 숫자로 변환
    year = Number(year)
    month = Number(month)
    day = Number(day)

    // 기본 유효성 검사
    if (year < 1900 || year > new Date().getFullYear()) return false
    if (month < 1 || month > 12) return false
    if (day < 1) return false

    // 월별 일수 체크
    const monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (isLeapYear(year)) {
        monthDays[1] = 29 // 윤년이면 2월은 29일
    }

    return day <= monthDays[month - 1]
}

// 이메일 유효성 검사 함수
const isValidEmail = (email) => {
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/
    return emailRegex.test(email)
}

// 필드 업데이트 함수
const updateField = (field, value) => {
    form.value[field] = value
    
    // 필드가 변경되면 해당 필드의 유효성 상태 초기화
    if (['userid', 'nickname', 'email'].includes(field)) {
        errors.value[field] = ''
        validations.value[field] = false
    }
    
    // 실시간 유효성 검사
    if (field === 'email' && value) {
        if (!isValidEmail(value)) {
            errors.value.email = '올바른 이메일 형식이 아닙니다.'
            validations.value.email = false
        } else {
            errors.value.email = ''
            validations.value.email = true
        }
    }

    // 비밀번호 실시간 유효성 검사
    if (field === 'password') {
        if (value.length < 6) {
            errors.value.password = '비밀번호는 6자 이상이어야 합니다.'
            validations.value.password = false
        } else {
            errors.value.password = ''
            validations.value.password = true
        }
        // 비밀번호 확인 필드도 다시 검사
        if (form.value.confirmPassword) {
            validatePasswordConfirm()
        }
    }

    // 비밀번호 확인 실시간 검사
    if (field === 'confirmPassword') {
        validatePasswordConfirm()
    }
}

// 비밀번호 확인 검사 함수
const validatePasswordConfirm = () => {
    if (!form.value.confirmPassword) {
        errors.value.confirmPassword = ''
        validations.value.confirmPassword = false
        return
    }
    
    if (form.value.password !== form.value.confirmPassword) {
        errors.value.confirmPassword = '비밀번호가 일치하지 않습니다.'
        validations.value.confirmPassword = false
    } else {
        errors.value.confirmPassword = ''
        validations.value.confirmPassword = true
    }
}

// 생년월일 유효성 검사 함수
const validateBirthDate = () => {
    const { birthYear, birthMonth, birthDay } = form.value
    
    if (!birthYear || !birthMonth || !birthDay) {
        errors.value.birthDate = ''
        validations.value.birthDate = false
        return
    }

    if (!isValidDate(birthYear, birthMonth, birthDay)) {
        errors.value.birthDate = '올바르지 않은 생년월일입니다.'
        validations.value.birthDate = false
    } else {
        errors.value.birthDate = ''
        validations.value.birthDate = true
    }
}

// 중복 체크 함수
const checkDuplicate = async (field) => {
    const value = form.value[field]
    if (!value) {
        errors.value[field] = `${field === 'userid' ? '아이디' : field === 'nickname' ? '닉네임' : '이메일'}를 입력해주세요.`
        validations.value[field] = false
        return
    }

    if (field === 'email' && !isValidEmail(value)) {
        errors.value.email = '올바른 이메일 형식이 아닙니다.'
        validations.value.email = false
        return
    }

    try {
        // GET 요청으로 변경하고 endpoint도 수정
        const endpoint = field === 'userid' ? 'check-id' : 'check-nickname'
        const response = await axios.create().get(`http://127.0.0.1:8000/api/v1/users/${endpoint}/`, {
            params: { value: value }
        })
        
        if (response.data.is_available) {
            errors.value[field] = ''
            validations.value[field] = true
        } else {
            errors.value[field] = `이미 사용 중인 ${field === 'userid' ? '아이디' : field === 'nickname' ? '닉네임' : '이메일'}입니다.`
            validations.value[field] = false
        }
    } catch (error) {
        console.error('중복 체크 에러:', error)
        errors.value[field] = '중복 체크 중 오류가 발생했습니다.'
        validations.value[field] = false
    }
}

// 폼 유효성 검사 수정
const validateForm = () => {
    if (!form.value.userid || !form.value.password) {
        alert('아이디와 비밀번호는 필수입니다!')
        return false
    }
    if (!validations.value.password) {
        alert('비밀번호는 6자 이상이어야 합니다.')
        return false
    }
    if (!validations.value.confirmPassword) {
        alert('비밀번호와 비밀번호 확인이 일치하지 않습니다!')
        return false
    }
    if (!form.value.name || !form.value.nickname || !form.value.email) {
        alert('이름, 닉네임, 이메일은 필수 입력사항입니다!')
        return false
    }
    if (!validations.value.email) {
        alert('올바른 이메일 형식이 아닙니다!')
        return false
    }
    if (!validations.value.birthDate) {
        alert('올바른 생년월일을 입력해주세요!')
        return false
    }
    if (!validations.value.userid || !validations.value.nickname || !validations.value.email) {
        alert('아이디, 닉네임, 이메일의 중복 확인이 필요합니다.')
        return false
    }
    return true
}

const ACCOUNT_API_URL = 'http://127.0.0.1:8000/api/v1/users' 

// 회원가입 함수
const onSignUp = async () => {
    if (!validateForm()) return

    const requestData = { ...form.value }
    console.log('회원가입 폼 데이터:', requestData)
    const success = await accountStore.signUp(requestData)
    
    // 회원가입 실패 시 폼 초기화하지 않고 유지
    if (!success) {
        return
    }
}
</script>

<style scoped>
.signup-container {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    padding-top: 2rem;
    background-color: #f5f5f5;
}

form {
    background-color: white;
    color: black;
    padding: 2rem;
    border-radius: 8px;
    width: 100%;
    max-width: 400px;
    font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

label {
    display: block;
    margin: 0.5rem 0 0.25rem;
    font-weight: 600;
    color: #333;
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
    margin-bottom: 0.25rem;
}

.birth-select select {
    flex: 1;
}

button[type="submit"] {
    margin-top: 1.5rem;
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

.input-group {
    position: relative;
    margin-bottom: 0.5rem;
}

.error-message {
    color: #dc3545;
    font-size: 0.85rem;
    margin-top: 0.1rem;
    display: block;
}

.success-message {
    color: #28a745;
    font-size: 0.85rem;
    margin-top: 0.1rem;
    display: block;
}

input.error {
    border-color: #dc3545;
}

input.success {
    border-color: #28a745;
}

input.error:focus {
    box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
}

input.success:focus {
    box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25);
}

select {
    margin-bottom: 0.5rem;
}
</style>
