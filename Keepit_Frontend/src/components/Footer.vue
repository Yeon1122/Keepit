<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section company-info">
        <img src="@/assets/images/logo_Keepit.png" alt="Keepit Logo" class="footer-logo">
        <p class="company-description">
          내 손 안의 금융비서, 킵잇
        </p>
        <div class="social-links">
          <a href="#" target="_blank" rel="noopener noreferrer"><i class="fab fa-instagram"></i></a>
          <a href="#" target="_blank" rel="noopener noreferrer"><i class="fab fa-facebook"></i></a>
          <a href="#" target="_blank" rel="noopener noreferrer"><i class="fab fa-youtube"></i></a>
        </div>
      </div>

      <div class="footer-section quick-links">
        <h3>바로가기</h3>
        <ul>
          <li><router-link to="/products/savings">예금/적금</router-link></li>
          <li><router-link to="/products/stocketf">주식/ETF</router-link></li>
          <li><router-link to="/products/goods">현물</router-link></li>
          <li><router-link to="/test">투자 성향 테스트</router-link></li>
        </ul>
      </div>

      <div class="footer-section community">
        <h3>커뮤니티</h3>
        <ul>
          <li><router-link to="/community/free">자유게시판</router-link></li>
          <li><router-link to="/question">질문게시판</router-link></li>
          <li><router-link to="/location">지점찾기</router-link></li>
          <li><router-link to="/chatbot">AI 챗봇</router-link></li>
        </ul>
      </div>

      <div class="footer-section contact">
        <h3>고객센터</h3>
        <p class="phone">1588-0000</p>
        <p class="work-hours">평일 09:00 - 18:00</p>
        <p class="work-hours">점심시간 12:00 - 13:00</p>
        <p class="work-hours">주말 및 공휴일 휴무</p>
      </div>
    </div>

    <div class="footer-bottom">
      <div class="footer-bottom-content">
        <div class="legal-links">
          <a href="#">이용약관</a>
          <a href="#" class="emphasis">개인정보처리방침</a>
          <a href="#">전자금융거래약관</a>
        </div>
        <p class="copyright">
          © 2025 Keepit. All rights will be reserved.
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
// No additional script needed
</script>

<style scoped>
.footer {
  background-color: #f8f9fa;
  padding-top: 3rem;
  margin-top: 4rem;
  border-top: 1px solid #eee;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.5fr;
  gap: 2rem;
}

.footer-section {
  margin-bottom: 2rem;
}

.company-info {
  padding-right: 2rem;
}

.footer-logo {
  height: 60px;
  margin-bottom: 1rem;
}

.company-description {
  color: #666;
  font-size: 0.75rem;
  line-height: 1.5;
  margin-bottom: 1.5rem;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-links a {
  color: #666;
  font-size: 1.5rem;
  transition: color 0.2s ease;
}

.social-links a:hover {
  color: #145c2b;
}

.footer-section h3 {
  color: #333;
  font-size: 1.1rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.footer-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-section ul li {
  margin-bottom: 0.8rem;
}

.footer-section ul li a {
  color: #666;
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.2s ease;
}

.footer-section ul li a:hover {
  color: #145c2b;
}

.contact .phone {
  font-size: 1.5rem;
  font-weight: 600;
  color: #145c2b;
  margin-bottom: 0.5rem;
}

.contact .work-hours {
  color: #666;
  font-size: 0.9rem;
  margin: 0.2rem 0;
}

.footer-bottom {
  background-color: #fff;
  padding: 1.5rem 0;
  margin-top: 2rem;
  border-top: 1px solid #eee;
}

.footer-bottom-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.legal-links {
  display: flex;
  gap: 1.5rem;
}

.legal-links a {
  color: #666;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s ease;
}

.legal-links a:hover {
  color: #145c2b;
}

.legal-links a.emphasis {
  font-weight: 600;
  color: #145c2b;
}

.copyright {
  color: #888;
  font-size: 0.9rem;
}

@media (max-width: 1024px) {
  .footer-content {
    grid-template-columns: 1fr 1fr;
  }

  .company-info {
    grid-column: 1 / -1;
    text-align: center;
    padding-right: 0;
  }

  .social-links {
    justify-content: center;
  }
}

@media (max-width: 640px) {
  .footer-content {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .footer-bottom-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .legal-links {
    flex-direction: column;
    gap: 0.8rem;
  }
}
</style>