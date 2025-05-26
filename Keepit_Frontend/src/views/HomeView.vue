<template>
  <div class="home">
    <div class="middle-1">
      <div class="left">
        <div class="picture">
          <img src="@/assets/images/Momo_test.png" alt="Keepit 캐릭터">
        </div>
      </div>
      <div class="right">
        <div class="content">
          <p class="subtitle">내 손 안의 금융비서</p>
          <h1 class="title">Keepit</h1>
          <p class="explain">간단한 테스트로 나에게 맞는 투자 성향과 금융 상품을 추천해드려요. <br> 나에게 꼭 맞는 금융 루틴, 지금 바로 시작해보세요!</p>
          <button class="go-to-test" @click="goToTest">
            투자 스타일 알아보기
            <span class="arrow">→</span>
          </button>
        </div>
      </div>
    </div>

    <div class="carousel">
      <div class="slides" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
        <div
          class="slide"
          v-for="(slide, index) in slideContents"
          :key="index"
          @click="handleSlideClick"
        >
          <div class="card">
            <div class="card-content">
              <span class="card-icon">
                {{ getIcon(index) }}
              </span>
              <h2>{{ slide[0] }}</h2>
              <p class="card-description">{{ getDescription(index) }}</p>
              <button class="card-button">자세히 보기</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/users.js'
import axios from 'axios'

const router = useRouter()
const accountStore = useAccountStore()
const slideContents = [
  ['정기 예금/적금'],
  ['현물'],
  ['주식/ETF'],
]

const currentIndex = ref(0)
let interval = null

const goToTest = async () => {
  console.log('🎯 투자 스타일 알아보기 버튼 클릭됨')
  
  // 로그인 확인
  if (!accountStore.isAuthenticated) {
    console.log('❌ 로그인되지 않음')
    if (confirm('투자 성향 검사를 받으려면 로그인이 필요합니다. 로그인 페이지로 이동하시겠습니까?')) {
      router.push({ name: 'login' })
    }
    return
  }

  console.log('✅ 로그인 확인됨, 검사 결과 확인 중...')

  try {
    // 기존 검사 결과 확인
    const response = await axios.get('/api/v1/test/result/')
    console.log('📊 검사 결과 응답:', response.data)
    
    if (response.data && response.data.type) {
      console.log('✅ 기존 검사 결과 있음:', response.data.type)
      // 기존 검사 결과가 있는 경우
      const userChoice = confirm('이미 투자 성향 검사를 받으셨습니다.\n\n다시 검사를 받으시겠습니까?\n\n확인: 새로 검사받기\n취소: 기존 결과 보기')
      console.log('👤 사용자 선택:', userChoice ? '새로 검사받기' : '기존 결과 보기')
      
      if (userChoice) {
        // 새로 검사받기
        router.push({ name: 'investmenttest' })
      } else {
        // 기존 결과 보기
        router.push({ name: 'testresult' })
      }
    } else {
      console.log('❌ 검사 결과 없음, 테스트로 이동')
      // 검사 결과가 없는 경우 바로 테스트로 이동
      router.push({ name: 'investmenttest' })
    }
  } catch (error) {
    console.error('❌ 검사 결과 확인 중 오류:', error)
    if (error.response?.status === 404) {
      console.log('📝 404 오류 - 검사 결과 없음, 테스트로 이동')
      // 검사 결과가 없는 경우 바로 테스트로 이동
      router.push({ name: 'investmenttest' })
    } else {
      console.error('🚨 기타 오류, 테스트로 이동')
      // 오류가 발생해도 테스트로 이동
      router.push({ name: 'investmenttest' })
    }
  }
}

const handleSlideClick = () => {
  const routeMap = {
    0: { name: 'savings' },    // 정기 예금/적금
    1: { name: 'goods' },      // 현물
    2: { name: 'stocks' },     // 주식/ETF
  }
  const route = routeMap[currentIndex.value]
  if (route) router.push(route)
}

const setSlide = (index) => {
  currentIndex.value = index
}

const getIcon = (index) => {
  const icons = ['💰', '💎', '📈']
  return icons[index]
}

const getDescription = (index) => {
  const descriptions = [
    '안정적인 수익을 원하는 분들을 위한 예금과 적금 상품을 만나보세요',
    '실물 자산에 투자하고 싶은 분들을 위한 현물 상품을 확인해보세요',
    '주식시장에서 수익을 추구하는 분들을 위한 다양한 상품이 준비되어 있어요'
  ]
  return descriptions[index]
}

onMounted(() => {
  interval = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % slideContents.length
  }, 4000)
})

onUnmounted(() => {
  clearInterval(interval)
})
</script>

<style scoped>
.home {
  min-height: 100vh;
  background-color: #ffffff;
}

.middle-1 {
  background: linear-gradient(to right, #f8f9fa 0%, #ffffff 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
}

.middle-1 > div {
  flex: 1;
}

.left {
  display: flex;
  justify-content: center;
  align-items: flex-end;
}

.right {
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.picture img {
  width: 400px;
  max-width: 100%;
  height: auto;
  transform: translateY(25px);
  filter: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.1));
}

.content {
  max-width: 480px;
  padding: 2rem;
}

.subtitle {
  font-size: 1.25rem;
  color: #145c2b;
  font-weight: 600;
  margin-bottom: 0.5rem;
  line-height: 1;
}

.title {
  margin: 0;
  font-size: 3.5rem;
  font-weight: 800;
  color: #145c2b;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.explain {
  font-size: 0.8rem;
  line-height: 2;
  color: #4a5568;
  margin-bottom: 2rem;
  word-break: keep-all;
  white-space: pre-line;
  max-width: 400px;
}

.go-to-test {
  background-color: #145c2b;
  color: white;
  border: none;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.arrow {
  color: white;
  transition: transform 0.3s ease;
}

.go-to-test:hover {
  background-color: #1a7436;
  transform: translateY(-2px);
}

.go-to-test:hover .arrow {
  transform: translateX(5px);
}

/* 캐러셀 스타일 */
.carousel {
  overflow: hidden;
  width: 100%;
  max-width: 1200px;
  margin: 4rem auto 0.5rem;
  border-radius: 16px;
  position: relative;
}

.slides {
  display: flex;
  transition: transform 0.5s ease-in-out;
}

.slide {
  min-width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  width: 100%;
  background: linear-gradient(135deg, #145c2b 0%, #1a7436 100%);
  padding: 3rem;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(20, 92, 43, 0.2);
}

.card-content {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

.card-content * {
  color: white;
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.card h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.card-description {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.card-button {
  background-color: white;
  color: #145c2b;
  border: none;
  padding: 0.8rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.card-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.carousel-indicators {
  display: none;
}

/* 반응형 디자인 */
@media (max-width: 968px) {
  .middle-1 {
    flex-direction: column;
    padding: 2rem;
  }

  .picture img {
    width: 300px;
    transform: translateY(0);
  }

  .content {
    text-align: center;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;  /* 내용물 중앙 정렬 */
  }

  .explain {
    margin: 0 auto;
    margin-bottom: 2rem;
    text-align: center;
  }

  .title {
    font-size: 2.5rem;
  }

  .go-to-test {
    margin: 0 auto;  /* 버튼 중앙 정렬 */
  }

  .card {
    padding: 2rem;
  }

  .card h2 {
    font-size: 2rem;
  }
}

.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  text-align: center;
}

.home-image {
  width: 200px;
  height: 200px;
  margin-bottom: 2rem;
}

.home-title {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #333;
}

.home-subtitle {
  font-size: 2.5rem;
  font-weight: bold;
  color: #145c2b;
  margin-bottom: 1.5rem;
}

.home-description {
  color: #666;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.start-button {
  display: inline-block;
  padding: 1rem 2rem;
  background-color: #145c2b;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: bold;
  transition: background-color 0.2s;
}

.start-button:hover {
  background-color: #0d4420;
}

/* 반응형 디자인 */
@media (min-width: 768px) {
  .home-container {
    padding: 4rem;
  }

  .home-image {
    width: 300px;
    height: 300px;
  }

  .home-title {
    font-size: 2.5rem;
  }

  .home-subtitle {
    font-size: 3rem;
  }
}

/* 작은 화면에서의 버튼 위치 조정 */
@media (max-width: 767px) {
  .home-container {
    padding: 2rem 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .start-button {
    margin: 0 auto;  /* 수평 중앙 정렬 */
  }
}
</style>
