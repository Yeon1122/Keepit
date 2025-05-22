<template>
  <form @submit.prevent="onUpdate">
    <label>이름:</label>
    <input type="text" v-model="form.name" />

    <label>닉네임:</label>
    <input type="text" v-model="form.nickname" />

    <label>이메일:</label>
    <input type="email" v-model="form.email" />

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

    <label>지역(시/도)</label>
    <select v-model="form.regionCity" @change="updateDistricts">
      <option disabled value="">선택하세요</option>
      <option v-for="region in mapInfo" :key="region.name" :value="region.name">{{ region.name }}</option>
    </select>

    <label>지역(시/구/군)</label>
    <select v-model="form.regionDistrict" :disabled="!form.regionCity">
      <option disabled value="">선택하세요</option>
      <option v-for="district in filteredDistricts" :key="district" :value="district">{{ district }}</option>
    </select>

    <button type="submit">정보 수정</button>
    <p class="delete-account" @click="onDelete">회원 탈퇴</p>
  </form>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAccountStore } from '@/stores/users.js'
import axios from 'axios'
import mapData from '@/assets/data/mapInfo.json'
import birthData from '@/assets/data/birthDropdown.json'
import { useRouter } from 'vue-router'

const accountStore = useAccountStore()
const { token } = accountStore
const router = useRouter()

const form = ref({
  name: '',
  nickname: '',
  email: '',
  birthYear: '',
  birthMonth: '',
  birthDay: '',
  regionCity: '',
  regionDistrict: ''
})

const mapInfo = ref(mapData.mapInfo)
const birthYears = ref(birthData.years)
const birthMonths = ref(birthData.months)
const birthDays = ref(birthData.days)

const filteredDistricts = computed(() => {
  const selected = mapInfo.value.find(region => region.name === form.value.regionCity)
  return selected ? selected.countries : []
})

const updateDistricts = () => {
  form.value.regionDistrict = ''
}

const onDelete = async () => {
  if (!confirm('정말로 탈퇴하시겠습니까? 😥')) return

  try {
    await axios.delete('http://127.0.0.1:8000/api/v1/users/mypage/', {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    alert('👋 회원 탈퇴가 완료되었습니다.')
    accountStore.logOut()
    router.push({ name: 'home' })
  } catch (err) {
    console.error('❌ 회원 탈퇴 실패:', err.response?.data || err.message)
    alert('회원 탈퇴에 실패했습니다.')
  }
}

onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/users/mypage/', {
      headers: {
        Authorization: `Token ${token}`
      }
    })

    const user = res.data
    form.value = {
      name: user.name,
      nickname: user.nickname,
      email: user.email,
      birthYear: user.birth_year,
      birthMonth: user.birth_month,
      birthDay: user.birth_day,
      regionCity: user.region_city,
      regionDistrict: user.region_district
    }
  } catch (err) {
    console.error('❌ 사용자 정보 불러오기 실패:', err)
  }
})

const onUpdate = async () => {
  try {
    const res = await axios.put('http://127.0.0.1:8000/api/v1/users/mypage/', form.value, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    alert('✅ 사용자 정보가 수정되었습니다.')
    router.push({ name: 'mypage' })
  } catch (err) {
    console.error('❌ 사용자 정보 수정 실패:', err.response?.data || err.message)
    alert('수정에 실패했습니다.')
  }
}
</script>

<style scoped>
form {
  background-color: white;
  color: black;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
  margin: auto;
  font-family: 'Pretendard', sans-serif;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

label {
  display: block;
  margin-top: 1rem;
  font-weight: 600;
}

input,
select {
  width: 100%;
  padding: 0.6rem 0.8rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  background-color: #f9f9f9;
  font-size: 0.95rem;
}

.birth-select {
  display: flex;
  gap: 0.5rem;
}

.birth-select select {
  flex: 1;
}

button[type='submit'] {
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

button[type='submit']:hover {
  background-color: #0e4a21;
}

.delete-account {
  margin-top: 2rem;
  text-align: center;
  font-size: 0.85rem;
  color: gray;
  cursor: pointer;
  text-decoration: underline;
}

.delete-account:hover {
  color: #d9534f;
  /* 빨간색으로 강조 */
}
</style>
