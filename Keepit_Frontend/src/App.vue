<template>
  <div>
    <div class="page-background">
      <div class="center-content">
        <header class="full-width">
          <div class="inner">
            <Header />
          </div>
        </header>

        <main class="container">
          <RouterView />
        </main>

        <footer class="full-width">
          <div class="inner">
            <Footer />
          </div>
        </footer>

        <FloatingButton />
      </div>
    </div>
    <MessageToast />
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import FloatingButton from '@/components/FloatingButton.vue'
import MessageToast from '@/components/MessageToast.vue'
</script>

<style>
/* Pretendard 폰트 import */
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css");

/* 전역 스타일 */
:root {
  /* 색상 변수 */
  --primary-color: #145c2b;
  --primary-dark: #0d4420;
  --text-primary: #333333;
  --text-secondary: #666666;
  --background-light: #f8f9fa;
  --border-color: #dddddd;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  line-height: 1.6;
  color: var(--text-primary);
  background-color: var(--background-light);
}

h1, h2, h3, h4, h5, h6, button {
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: var(--text-primary);
}

/* 숫자, 금액 표시에 Pretendard 적용 */
.number {
  font-family: 'Pretendard', sans-serif;
  font-feature-settings: "tnum";
  font-variant-numeric: tabular-nums;
}

/* 버튼 기본 스타일 */
button {
  font-family: 'Pretendard', sans-serif;
  cursor: pointer;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.2s ease;
}

button.primary {
  background-color: var(--primary-color);
  color: white;
}

button.primary:hover {
  background-color: var(--primary-dark);
}

/* 입력 필드 기본 스타일 */
input, select, textarea {
  font-family: 'Pretendard', sans-serif;
  padding: 0.8rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

.page-background {
  background-color: #f5f5f5;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 2rem 0;
  box-sizing: border-box;
}

/* 전체 중앙 정렬 영역 */
.center-content {
  width: 100%;
  max-width: 960px;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
}

/* Header와 Footer 배경이 흰색 유지되도록 */
.full-width {
  width: 100%;
  background-color: #ffffff;
}

/* Header/Footer 내부 여백 */
.inner {
  padding: 1rem 2rem;
  box-sizing: border-box;
}

/* 메인 콘텐츠 중앙 정렬 + 회색 배경 강조 가능 */
.container {
  width: 100%;
  box-sizing: border-box;
  background-color: #f9f9f9;
  /* 원하시면 제거 가능 */
  border-radius: 8px;
}
</style>