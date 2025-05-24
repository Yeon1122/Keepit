<template>
  <div class="location-overlay" @click.self="closeModal">
    <div class="location-modal">
      <div class="modal-header">
        <h2>은행 찾기</h2>
        <button class="close-button" @click="closeModal">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="search-container">
        <div class="search-box">
          <div class="input-group">
            <label>광역시/도</label>
            <select v-model="selectedSido" @change="onSidoChange">
              <option value="">광역시/도를 선택하세요</option>
              <option v-for="sido in sidoList" :key="sido" :value="sido">{{ sido }}</option>
            </select>
          </div>

          <div class="input-group">
            <label>시/군/구</label>
            <select v-model="selectedSigungu" :disabled="!selectedSido">
              <option value="">시/군/구를 선택하세요</option>
              <option v-for="sigungu in sigunguList" :key="sigungu" :value="sigungu">{{ sigungu }}</option>
            </select>
          </div>

          <div class="input-group">
            <label>은행</label>
            <select v-model="selectedBank">
              <option value="">은행을 선택하세요</option>
              <option v-for="bank in bankList" :key="bank" :value="bank">{{ bank }}</option>
            </select>
          </div>

          <button class="search-button" @click="searchBanks" :disabled="!isSearchable">
            <i class="fas fa-search"></i> 검색
          </button>
        </div>

        <div id="map" class="map-container"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import mapInfo from '@/assets/data/mapInfo.json'

const router = useRouter()
const selectedSido = ref('')
const selectedSigungu = ref('')
const selectedBank = ref('')
let map = null
let markers = []

// mapInfo.json에서 데이터 가져오기
const sidoList = mapInfo.mapInfo.map(region => region.name)
const sigunguMap = Object.fromEntries(
  mapInfo.mapInfo.map(region => [region.name, region.countries])
)
const bankList = mapInfo.bankInfo

const sigunguList = computed(() => {
  return selectedSido.value ? sigunguMap[selectedSido.value] || [] : []
})

const isSearchable = computed(() => {
  return selectedSido.value && selectedSigungu.value && selectedBank.value
})

const closeModal = () => {
  router.back()
}

const initMap = () => {
  if (window.kakao && window.kakao.maps) {
    const container = document.getElementById('map')
    const options = {
      center: new window.kakao.maps.LatLng(37.5665, 126.9780),
      level: 3
    }
    map = new window.kakao.maps.Map(container, options)
  }
}

const searchBanks = () => {
  if (!map || !window.kakao) return

  // 기존 마커 제거
  markers.forEach(marker => marker.setMap(null))
  markers = []

  const ps = new window.kakao.maps.services.Places()
  const searchKeyword = `${selectedSido.value} ${selectedSigungu.value} ${selectedBank.value}`

  ps.keywordSearch(searchKeyword, (data, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      const bounds = new window.kakao.maps.LatLngBounds()

      data.forEach(place => {
        const position = new window.kakao.maps.LatLng(place.y, place.x)
        const marker = new window.kakao.maps.Marker({
          map: map,
          position: position
        })

        markers.push(marker)
        bounds.extend(position)

        // 정보창 생성
        const infowindow = new window.kakao.maps.InfoWindow({
          content: `
            <div class="info-window">
              <h3>${place.place_name}</h3>
              <p>${place.address_name}</p>
              <p>${place.phone || '전화번호 없음'}</p>
            </div>
          `
        })

        // 마커 클릭 이벤트
        window.kakao.maps.event.addListener(marker, 'click', () => {
          infowindow.open(map, marker)
        })
      })

      map.setBounds(bounds)
    }
  })
}

const onSidoChange = () => {
  selectedSigungu.value = ''
}

onMounted(() => {
  // 카카오맵 스크립트 로드
  const script = document.createElement('script')
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_API_KEY}&libraries=services`
  script.async = true
  script.onload = initMap
  document.head.appendChild(script)
})
</script>

<style scoped>
.location-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.location-modal {
  background: white;
  width: 90%;
  max-width: 1200px;
  height: 80vh;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.modal-header h2 {
  color: #145c2b;
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #666;
  cursor: pointer;
  padding: 0.5rem;
  transition: color 0.2s;
}

.close-button:hover {
  color: #145c2b;
}

.search-container {
  display: flex;
  gap: 2rem;
  height: calc(100% - 4rem);
}

.search-box {
  width: 300px;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-group label {
  font-weight: 500;
  color: #333;
}

select {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

select:focus {
  outline: none;
  border-color: #145c2b;
}

select:disabled {
  background: #f1f1f1;
  cursor: not-allowed;
}

.search-button {
  background: #145c2b;
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: auto;
}

.search-button:hover:not(:disabled) {
  background: #0d4420;
}

.search-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.map-container {
  flex: 1;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* 정보창 스타일 */
:deep(.info-window) {
  padding: 0.5rem;
  min-width: 200px;
}

:deep(.info-window h3) {
  margin: 0 0 0.5rem 0;
  color: #145c2b;
  font-size: 1rem;
}

:deep(.info-window p) {
  margin: 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}
</style> 