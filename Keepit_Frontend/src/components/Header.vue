<template>
    <header class="header">
        <div class="logo-box" @click="goHome" style="cursor: pointer;">
            <img src="@/assets/images/logo_2.png" alt="Keepit Logo" class="logo">
        </div>

        <nav class="navbar">
            <ul class="nav-menu">
                <li><a href="#">금융비서</a></li>
                <li><a href="#">상품안내</a></li>
                <li><a href="#">커뮤니티</a></li>
            </ul>

            <div class="dropdown-container">
                <div class="dropdown-group">
                    <ul>
                        <li class="middle">투자 성향 분석</li>
                        <li><a href="#">투자 스타일 알아보기</a></li>
                        <li><a href="#">투자 성향 결과</a></li>
                    </ul>
                    <ul>
                        <li class="middle">상품 비교</li>
                        <li><a href="#">정기 예금</a></li>
                        <li><a href="#">적금</a></li>
                    </ul>
                </div>
                <div class="dropdown-group">
                    <ul>
                        <li><a href="#">정기 예금/적금</a></li>
                        <li><a href="#">현물</a></li>
                        <li><a href="#">주식/ETF</a></li>
                    </ul>
                </div>
                <div class="dropdown-group">
                    <ul>
                        <li><a href="#">자유 게시판</a></li>
                        <li><a href="#">질문 게시판</a></li>
                        <li><a href="#">뉴스</a></li>
                    </ul>
                </div>
            </div>
        </nav>

        <div class="btns" v-if="!isLoggedIn">
            <!-- 비로그인 시 -->
            <button class="login btn-1" @click="goToLogin">Login</button>
            <button class="get-started btn-2" @click="goToSignup">Get Started</button>
        </div>

        <div class="btns" v-else>
            <!-- 로그인 시 -->
            <button class="login btn-1">마이페이지</button>
            <button class="get-started btn-2">로그아웃</button>
        </div>
    </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
    router.push({ name: 'home' })
    // console.log('move to home')
}

const goToSignup = () => {
    router.push({ name: 'signup' })
    // console.log('move to signup')
}

const goToLogin = () => {
    router.push({ name: 'login' })
    // console.log('move to signup')
}

// ✅ 로그인 여부 상태 (예시로 false로 초기화)
const isLoggedIn = ref(false)
</script>

<style scoped>
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: white;
    border-bottom: 1px solid #ccc;
    position: relative;
}

.logo-box {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.logo {
    width: 100px;
    height: auto;
}

.navbar {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-right: 2rem;
}

.nav-menu {
    list-style: none;
    display: flex;
    gap: 0;
    /* ✅ gap 제거 */
    padding: 0;
    margin: 0;
}

.nav-menu li {
    margin-right: 0;
    margin: 0px;
    /* 기본 초기화 */
}

/* 개별 간격 지정 */
.nav-menu li:nth-child(1) {
    margin-left: 35px;
    margin-right: 100px;
    /* 금융비서 → 상품안내 */
}

.nav-menu li:nth-child(2) {
    margin-right: 100px;
    /* 상품안내 → 커뮤니티 */
}

.middle {
    font-weight: bold;
    font-size: 1rem;
    color: #000;
}

.nav-menu li a {
    font-weight: bold;
    color: #333;
    text-decoration: none;
    font-size: 1rem;
}

.dropdown-group:nth-child(1) {
    margin-left: 5px;
    margin-right: 2rem;
}

.dropdown-group:nth-child(2) {
    margin-right: 4.2rem;
}

/* 드롭다운 전체 박스 */
.dropdown-container {
    display: none;
    /* 기본은 숨김 */
    position: absolute;
    top: 100%;
    left: 0;
    background-color: white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 2rem 2rem;
    width: 100%;
    justify-content: flex-start;
    gap: 0;
    z-index: 10;
}

.navbar:hover .dropdown-container {
    display: flex;
    /* navbar에 hover 시 나타남 */
}

.dropdown-group ul {
    list-style: none;
    padding: 0;
    font-size: 0.9rem;
}

.dropdown-group li {
    margin: 1rem 0;
}

.dropdown-group a {
    color: #555;
    /* 링크 색상 회색 */
    text-decoration: none;
}

.dropdown-group a:hover {
    color: #222;
    text-decoration: underline;
}

.btns {
    display: flex;
    gap: 1rem;
    align-items: center;
}

.btn-1 {
    background: white;
    border: 1px solid #145c2b;
    color: #145c2b;
    padding: 0.4rem 1rem;
    font-weight: bold;
    border-radius: 6px;
    cursor: pointer;
}

.btn-2 {
    background: #145c2b;
    border: none;
    color: white;
    padding: 0.4rem 1rem;
    font-weight: bold;
    border-radius: 6px;
    cursor: pointer;
}
</style>
