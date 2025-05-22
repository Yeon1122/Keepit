import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
    const router = useRouter()
    const token = ref('')
    const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'

    const signUp = function (payload) {
        axios({
            method: 'POST',
            url: `${ACCOUNT_API_URL}/signup/`,
            data: {
                username: payload.userid,
                password1: payload.password,
                password2: payload.password,
                name: payload.name,
                nickname: payload.nickname,
                email: payload.email,
                birth_year: Number(payload.birthYear),
                birth_month: Number(payload.birthMonth),
                birth_day: Number(payload.birthDay),
                income_range: payload.incomeRange,
                region_city: payload.regionCity,
                region_district: payload.regionDistrict,
            }
        })
            .then(res => {
                console.log('✅ 회원가입 성공!', res.data)
                alert('회원가입이 완료되었습니다.')
                router.push({ name: 'home' })
            })
            .catch(err => {
                console.error('❌ 회원가입 실패', err.response?.data || err.message)
                alert('회원가입에 실패했습니다.')
            })
    }

    const logIn = function ({ username, password }) {
        axios({
            method: 'POST',
            url: `${ACCOUNT_API_URL}/login/`,
            data: { username, password }
        })
            .then(res => {
                token.value = res.data.key
                console.log('✅ 로그인 성공')
                router.push({ name: 'home' })
            })
            .catch(err => {
                console.error('❌ 로그인 실패', err.response?.data || err.message)
                alert('로그인 실패! 아이디/비밀번호를 확인하세요.')
            })
    }

    return {
        token,
        signUp,
        logIn
    }
}, { persist: true })

