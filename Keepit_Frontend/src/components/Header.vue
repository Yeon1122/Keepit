<template>
    <header class="header">
        <div class="header-content">
            <div class="logo-box" @click="goHome">
                <img src="@/assets/images/logo_Keepit.png" alt="Keepit Logo" class="logo">
            </div>

            <nav class="navbar" @mouseleave="hideDropdown">
                <ul class="nav-menu" @mouseenter="showDropdown">
                    <li class="nav-item">
                        <a href="#" class="nav-link">금융비서</a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link">상품안내</a>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link">커뮤니티</a>
                    </li>
                </ul>

                <!-- 통합 드롭다운 메뉴 -->
                <div class="mega-dropdown" v-show="isDropdownVisible" :class="{ 'show': isDropdownVisible }">
                    <div class="mega-content">
                        <!-- 금융비서 섹션 -->
                        <div class="mega-section">
                            <div class="section-group">
                                <div class="section-title">투자 성향 분석</div>
                                <ul class="dropdown-menu">
                                    <li><router-link :to="{ name: 'investmenttest' }">투자 스타일 알아보기</router-link></li>
                                    <li><router-link :to="{ name: 'testresult' }">투자 성향 결과</router-link></li>
                                </ul>
                            </div>
                            <div class="section-group">
                                <div class="section-title">상품 비교</div>
                                <ul class="dropdown-menu menu-1">
                                    <li><router-link :to="{ name: 'compare', query: { type: 'deposit' } }">정기 예금</router-link></li>
                                    <li><router-link :to="{ name: 'compare', query: { type: 'saving' } }">적금</router-link></li>
                                </ul>
                            </div>
                        </div>

                        <!-- 상품안내 섹션 -->
                        <div class="mega-section">
                            <ul class="dropdown-menu menu-2">
                                <li><router-link :to="{ name: 'savings' }">정기 예금/적금</router-link></li>
                                <li><router-link :to="{ name: 'goods' }">현물</router-link></li>
                                <li><router-link :to="{ name: 'stocks' }">주식/ETF</router-link></li>
                            </ul>
                        </div>

                        <!-- 커뮤니티 섹션 -->
                        <div class="mega-section">
                            <ul class="dropdown-menu menu-3">
                                <li><router-link :to="{ name: 'freecommunity' }">자유 게시판</router-link></li>
                                <li><router-link :to="{ name: 'questioncommunity' }">질문 게시판</router-link></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </nav>

            <div class="auth-buttons" v-if="!isLoggedIn">
                <button class="btn-login" @click="goToLogin">로그인</button>
                <button class="btn-signup" @click="goToSignup">회원가입</button>
            </div>

            <div class="auth-buttons" v-else>
                <button class="btn-logout" @click="handleLogout">로그아웃</button>
                <button class="btn-mypage" @click="goToMypage">마이페이지</button>
            </div>
        </div>
    </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/users.js'

const router = useRouter()
const accountStore = useAccountStore()
const isLoggedIn = computed(() => accountStore.isAuthenticated)

// 드롭다운 메뉴 상태 관리
const isDropdownVisible = ref(false)

const showDropdown = () => {
    isDropdownVisible.value = true
}

const hideDropdown = () => {
    isDropdownVisible.value = false
}

const goHome = () => router.push({ name: 'home' })
const goToSignup = () => router.push({ name: 'signup' })
const goToLogin = () => router.push({ name: 'login' })
const goToMypage = () => router.push({ name: 'mypage' })
const handleLogout = () => {
    accountStore.logOut()
    router.push({ name: 'home' })
}
</script>

<style scoped>
.header {
  background-color: white;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 0;
  z-index: 1000;
  padding: 0.5rem 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.logo-box {
  cursor: pointer;
}

.logo {
  width: 120px;
  height: auto;
}

/* 네비게이션 메뉴 */
.navbar {
  flex: 1;
  margin: 0 2rem;
  display: flex;
  justify-content: center;
  position: relative;
}

.nav-menu {
  list-style: none;
  display: flex;
  gap: 5rem;
  margin: 0;
  padding: 0;
  justify-content: center;
}

.nav-item {
  position: relative;
}

.nav-link {
  font-family: 'Pretendard', sans-serif;
  font-weight: 500;
  font-size: 1.05rem;
  color: #333;
  text-decoration: none;
  padding: 0.8rem 0;
  transition: color 0.2s;
  white-space: nowrap;
}

.nav-link:hover {
  color: var(--primary-color);
}

/* ✅ 드롭다운 메뉴 */
.mega-dropdown {
  position: absolute;
  top: calc(100% + 5px);
  left: -20px;
  transform: none;
  width: max-content;
  background: white;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s;
  z-index: 1000;
  border-top: 1px solid #eee;
}

.mega-dropdown.show {
  opacity: 1;
  visibility: visible;
}

.mega-content {
  display: grid;
  grid-template-columns: auto auto auto;
  column-gap: 1.5rem;
  padding: 2rem 1.2rem;
  align-items: start;
}

.mega-section {
  min-width: 110px;
  display: flex;
  flex-direction: column;
}

.section-group {
  margin-bottom: 1rem;
}

.section-title {
  font-family: 'Pretendard', sans-serif;
  font-weight: 600;
  font-size: 1rem;
  color: var(--primary-color);
  padding-bottom: 0.5rem;
  margin-bottom: 0.8rem;
  border-bottom: 2px solid var(--primary-color);
}

.dropdown-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.dropdown-menu li {
  margin: 0.6rem 0;
}

.menu-2,
.menu-3 {
  padding-right: 0.1rem;
  margin-right: 0;
}

.dropdown-menu a {
  font-size: 0.95rem;
  color: #666;
  text-decoration: none;
  transition: color 0.2s;
}

.dropdown-menu a:hover {
  color: var(--primary-color);
}

/* 인증 버튼 */
.auth-buttons {
  display: flex;
  gap: 1rem;
}

.btn-login,
.btn-logout {
  padding: 0.5rem 1.2rem;
  border: 2px solid #145c2b;
  border-radius: 8px;
  background-color: white;
  color: #145c2b;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-login:hover,
.btn-logout:hover {
  background-color: #f8f8f8;
}

.btn-signup,
.btn-mypage {
  padding: 0.5rem 1.2rem;
  border: 2px solid #145c2b;
  border-radius: 8px;
  background-color: #145c2b;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-signup:hover,
.btn-mypage:hover {
  background-color: #0d3d1d;
  border-color: #0d3d1d;
}

/* ✅ PC 화면 최적화 (768px 이상일 때 조정) */
@media (min-width: 769px) {
  .mega-dropdown {
    left: -40px; /* 조금 더 오른쪽으로 이동 */
  }

  .mega-content {
    column-gap: 2.5rem; /* 열 간격 넓힘 */
    padding: 2rem 2rem;
  }

  .mega-section {
    min-width: 130px; /* PC에선 넓게 */
  }
}
</style>

