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
      </div>
    </div>
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
</script>

<style>
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