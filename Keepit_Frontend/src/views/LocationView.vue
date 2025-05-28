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
              <option value="전체">전체</option>
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
import { useAccountStore } from '@/stores/users.js'
import axios from 'axios'

const router = useRouter()
const accountStore = useAccountStore()
const selectedSido = ref('')
const selectedSigungu = ref('')
const selectedBank = ref('전체')
let map = null
let markers = []
let currentInfoWindow = null  // 현재 열린 정보창을 추적하기 위한 변수

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
  return selectedSido.value && selectedSigungu.value
})

// 삼성화재 대전유성캠퍼스 좌표
const DEFAULT_CENTER = {
  lat: 36.3554,  // 대전 유성구 삼성화재 유성캠퍼스 위도
  lng: 127.2983  // 대전 유성구 삼성화재 유성캠퍼스 경도
}

// 사용자 지역 정보 가져오기
const getUserLocation = async () => {
  if (!accountStore.isAuthenticated) {
    return DEFAULT_CENTER
  }

  try {
    const response = await axios.get('/api/v1/users/mypage/', {
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })

    if (response.data.region_city && response.data.region_district) {
      selectedSido.value = response.data.region_city
      selectedSigungu.value = response.data.region_district
      
      return new Promise((resolve) => {
        const geocoder = new kakao.maps.services.Geocoder()
        const address = `${response.data.region_city} ${response.data.region_district}`
        
        geocoder.addressSearch(address, (result, status) => {
          if (status === kakao.maps.services.Status.OK) {
            resolve({
              lat: parseFloat(result[0].y),
              lng: parseFloat(result[0].x)
            })
          } else {
            console.log('주소 -> 좌표 변환 실패, 기본 위치 사용')
            resolve(DEFAULT_CENTER)
          }
        })
      })
    }
  } catch (error) {
    console.error('사용자 위치 정보 가져오기 실패:', error)
  }
  return DEFAULT_CENTER
}

const closeModal = () => {
  router.back()
}

const initMap = async () => {
  console.log('📍 initMap 실행됨')
  console.log('🔍 map container 찾기 시도...')

  if (!import.meta.env.VITE_KAKAO_MAP_API_KEY) {
    console.error('카카오맵 API 키가 설정되지 않았습니다.')
    alert('지도 서비스를 사용할 수 없습니다. 관리자에게 문의해주세요.')
    return
  }

  try {
    const container = document.getElementById('map')
    if (!container) {
      console.error('❌ 지도를 표시할 div를 찾을 수 없습니다.')
      console.log('🔍 DOM 상태:', document.readyState)
      console.log('🔍 body 내용:', document.body.innerHTML.includes('map'))
      return
    }
    
    console.log('✅ map container 찾음:', container)
    console.log('📏 container 크기:', container.offsetWidth, 'x', container.offsetHeight)

    // 초기 중심 좌표 설정
    const center = await getUserLocation()
    console.log('📍 중심 좌표:', center)

    console.log('🗺️ 카카오맵 생성 시도...')
    const options = {
      center: new kakao.maps.LatLng(center.lat, center.lng),
      level: 5
    }

    map = new kakao.maps.Map(container, options)
    console.log('✅ 카카오맵 생성 완료:', map)
    
    // 확대/축소 컨트롤 추가
    const zoomControl = new kakao.maps.ZoomControl()
    map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT)
    console.log('🎛️ 확대/축소 컨트롤 추가됨')
    
    // 지도 클릭 시 열린 정보창 닫기
    kakao.maps.event.addListener(map, 'click', () => {
      if (currentInfoWindow) {
        currentInfoWindow.close()
        currentInfoWindow = null
      }
    })

    // 사용자 위치에 마커 표시
    if (center !== DEFAULT_CENTER) {
      const marker = new kakao.maps.Marker({
        position: new kakao.maps.LatLng(center.lat, center.lng),
        map: map
      })
      
      const infowindow = new kakao.maps.InfoWindow({
        content: '<div style="padding:5px;">현재 설정된 지역</div>'
      })
      
      kakao.maps.event.addListener(marker, 'click', () => {
        // 이전에 열린 정보창이 있다면 닫기
        if (currentInfoWindow) {
          currentInfoWindow.close()
        }
        infowindow.open(map, marker)
        currentInfoWindow = infowindow
      })
    }
  } catch (error) {
    console.error('❌ 지도 초기화 실패:', error)
    console.error('❌ 에러 스택:', error.stack)
    alert('지도를 불러오는데 실패했습니다. 페이지를 새로고침 해주세요.')
  }
}

const searchBanks = () => {
  if (!map || !kakao) {
    alert('지도가 아직 로드되지 않았습니다. 잠시 후 다시 시도해주세요.')
    return
  }

  // 기존 마커와 정보창 제거
  markers.forEach(marker => marker.setMap(null))
  if (currentInfoWindow) {
    currentInfoWindow.close()
    currentInfoWindow = null
  }
  markers = []

  const ps = new kakao.maps.services.Places()
  const searchKeyword = selectedBank.value === '전체' 
    ? `${selectedSido.value} ${selectedSigungu.value} 은행`
    : `${selectedSido.value} ${selectedSigungu.value} ${selectedBank.value}`

  console.log('🔍 검색 키워드:', searchKeyword)

  ps.keywordSearch(searchKeyword, (data, status) => {
    if (status === kakao.maps.services.Status.OK) {
      if (data.length === 0) {
        alert('검색 결과가 없습니다. 다른 지역이나 은행을 선택해주세요.')
        return
      }

      const bounds = new kakao.maps.LatLngBounds()

      data.forEach(place => {
        const position = new kakao.maps.LatLng(place.y, place.x)
        const marker = new kakao.maps.Marker({
          map: map,
          position: position
        })

        markers.push(marker)
        bounds.extend(position)

        // 정보창 생성
        const infowindow = new kakao.maps.InfoWindow({
          content: `
            <div class="info-window">
              <h5>${place.place_name}</h5>
              <p>${place.address_name}</p>
            </div>
          `
        })

        // 마커 클릭 이벤트
        kakao.maps.event.addListener(marker, 'click', () => {
          // 이전에 열린 정보창이 있다면 닫기
          if (currentInfoWindow) {
            currentInfoWindow.close()
          }
          infowindow.open(map, marker)
          currentInfoWindow = infowindow
        })
      })

      map.setBounds(bounds)
    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
      alert('검색 결과가 없습니다. 다른 지역이나 은행을 선택해주세요.')
    } else {
      alert('검색 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
    }
  })
}

const onSidoChange = () => {
  selectedSigungu.value = ''
}

onMounted(() => {
  console.log('🚀 LocationView 마운트됨')
  console.log('🔑 KAKAO API KEY:', import.meta.env.VITE_KAKAO_MAP_API_KEY ? '설정됨' : '설정되지 않음')
  
  if (!import.meta.env.VITE_KAKAO_MAP_API_KEY) {
    console.error('❌ 카카오맵 API 키가 환경변수에 설정되지 않았습니다.')
    alert('카카오맵 API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.')
    return
  }

  const script = document.createElement('script')
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_API_KEY}&autoload=false&libraries=services`
  script.async = true
  
  script.onload = () => {
    console.log('✅ 카카오맵 스크립트 로드됨')
    console.log('🌐 kakao 객체 존재:', typeof kakao !== 'undefined')
    
    if (typeof kakao === 'undefined') {
      console.error('❌ kakao 객체가 정의되지 않았습니다.')
      alert('카카오맵 스크립트 로딩에 실패했습니다.')
      return
    }
    
    kakao.maps.load(async () => {
      console.log('🗺️ kakao.maps SDK 로딩 완료')
      console.log('🗺️ kakao.maps 객체:', kakao.maps)
      await initMap()
    })
  }
  
  script.onerror = (error) => {
    console.error('❌ 카카오맵 스크립트 로딩 실패:', error)
    alert('카카오맵 스크립트를 불러오는데 실패했습니다. 네트워크 연결을 확인해주세요.')
  }
  
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
  min-height: 400px; /* ✅ 꼭 필요 */
  height: 100%; 
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

#map {
  width: 100%;
  height: 100%;
  min-height: 400px; /* 필수 */
}

/* 정보창 스타일 */
:deep(.info-window) {
  padding: 0.5rem;
  min-width: 200px;
}

:deep(.info-window h5) {
  margin: 0 0 0.5rem 0;
  color: #145c2b;
  font-size: 1rem;
}

:deep(.info-window p) {
  margin: 0.25rem 0;
  color: #666;
  font-size: 0.68rem;
}
</style> 