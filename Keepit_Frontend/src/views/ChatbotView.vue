<template>
  <div class="chatbot-overlay" @click.self="closeModal">
    <div class="chatbot-modal">
      <div class="modal-header">
        <div class="header-content">
          <img src="@/assets/images/Momo_chatbot.png" alt="Momo AI" class="chatbot-avatar">
          <h2>AI 챗봇 모모</h2>
        </div>
        <button class="close-button" @click="closeModal">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <div class="chat-container">
        <div class="chat-messages" ref="messageContainer">
          <div v-for="(message, index) in messages" :key="index"
            :class="['message', message.type === 'user' ? 'user-message' : 'bot-message']">
            <div class="message-content">
              <p>{{ message.text }}</p>
            </div>
          </div>
          <div v-if="isLoading" class="bot-message">
            <div class="message-content">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>

        <div class="chat-input">
          <div class="quick-buttons" v-if="showQuickButtons">
            <button @click="handleQuickButton('문의하기')" class="quick-button">
              문의하기
            </button>
            <button @click="handleQuickButton('상품 질문하기')" class="quick-button">
              상품 질문하기
            </button>
          </div>
          <div class="input-container" v-else>
            <input 
              type="text" 
              v-model="userInput" 
              @keyup.enter="sendMessage"
              placeholder="메시지를 입력하세요..."
              :disabled="isLoading"
            >
            <button @click="sendMessage" :disabled="!userInput.trim() || isLoading">
              <i class="fas fa-paper-plane"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const messageContainer = ref(null)
const userInput = ref('')
const messages = ref([])
const isLoading = ref(false)
const showQuickButtons = ref(true)
let chatSession = null

const closeModal = () => {
  router.back()
}

const scrollToBottom = async () => {
  await nextTick()
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
}

const handleQuickButton = async (type) => {
  console.log('🔘 Quick button clicked:', type)
  try {
    showQuickButtons.value = false
    messages.value.push({ type: 'user', text: type })
    await scrollToBottom()
    await sendToChatbot(type)
  } catch (error) {
    console.error('❌ Quick button error:', error)
    showQuickButtons.value = true // 에러 시 버튼 다시 표시
  }
}

const sendMessage = async () => {
  console.log('📤 Send message clicked, input:', userInput.value)
  if (!userInput.value.trim() || isLoading.value) {
    console.log('❌ Message blocked - empty or loading')
    return
  }

  try {
    const message = userInput.value
    userInput.value = ''
    messages.value.push({ type: 'user', text: message })
    await scrollToBottom()
    await sendToChatbot(message)
  } catch (error) {
    console.error('❌ Send message error:', error)
  }
}

const sendToChatbot = async (message) => {
  console.log('🤖 Sending to chatbot:', message)
  isLoading.value = true
  await scrollToBottom()

  try {
    let response
    if (!chatSession) {
      console.log('🆕 Starting new chat session')
      
      // 버튼에 따라 카테고리 결정
      let category = 'product_info' // 기본값
      if (message === '문의하기') {
        category = 'page_help'
      } else if (message === '상품 질문하기') {
        category = 'product_info'
      }
      
      // 채팅 세션 시작
      response = await axios.post('/api/v1/chatbot/start/', {
        category: category
      })
      chatSession = response.data.session_id
      console.log('✅ Chat session created:', chatSession, 'with category:', category)
      
      // 환영 메시지는 이미 백엔드에서 생성되므로 추가
      if (response.data.welcome_message) {
        messages.value.push({ type: 'bot', text: response.data.welcome_message })
      }
      
      // 첫 메시지가 환영 메시지가 아닌 경우에만 사용자 메시지 처리
      if (message !== '문의하기' && message !== '상품 질문하기') {
        response = await axios.post(`/api/v1/chatbot/chat/${chatSession}/`, {
          message: message
        })
        messages.value.push({ type: 'bot', text: response.data.response })
      }
    } else {
      console.log('💬 Continuing existing session:', chatSession)
      // 기존 세션에 메시지 전송
      response = await axios.post(`/api/v1/chatbot/chat/${chatSession}/`, {
        message: message
      })
      console.log('📨 Chatbot response:', response.data)
      // 챗봇 응답 추가
      messages.value.push({ type: 'bot', text: response.data.response })
    }
  } catch (error) {
    console.error('❌ Chatbot API error:', error)
    console.error('❌ Error details:', error.response?.data)
    messages.value.push({ 
      type: 'bot', 
      text: '죄송합니다. 서버 연결에 문제가 있습니다. 잠시 후 다시 시도해주세요.' 
    })
  }

  isLoading.value = false
  await scrollToBottom()
}

onMounted(() => {
  messages.value.push({ 
    type: 'bot', 
    text: '안녕하세요! 킵잇 AI 챗봇 모모입니다. 무엇을 도와드릴까요?' 
  })
})
</script>

<style scoped>
.chatbot-overlay {
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

.chatbot-modal {
  background: white;
  width: 90%;
  max-width: 500px;
  height: 600px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.chatbot-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.modal-header h2 {
  color: #145c2b;
  margin: 0;
  font-size: 1.2rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #666;
  cursor: pointer;
  padding: 0.5rem;
  transition: color 0.2s;
}

.close-button:hover {
  color: #145c2b;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  display: flex;
  margin-bottom: 0.5rem;
}

.user-message {
  justify-content: flex-end;
}

.bot-message {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 0.8rem 1rem;
  border-radius: 12px;
  font-size: 0.95rem;
}

.user-message .message-content {
  background: #145c2b;
  color: white;
  border-bottom-right-radius: 4px;
}

.bot-message .message-content {
  background: #f0f0f0;
  color: #333;
  border-bottom-left-radius: 4px;
}

.message-content p {
  margin: 0;
  line-height: 1.4;
}

.chat-input {
  padding: 1rem;
  border-top: 1px solid #eee;
}

.input-container {
  display: flex;
  gap: 0.5rem;
}

.input-container input {
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.input-container input:focus {
  outline: none;
  border-color: #145c2b;
}

.input-container button {
  background: #145c2b;
  color: white;
  border: none;
  padding: 0 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.input-container button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.input-container button:hover:not(:disabled) {
  background: #0d4420;
}

.quick-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.quick-button {
  padding: 0.8rem 1.5rem;
  border: 2px solid #145c2b;
  background: white;
  color: #145c2b;
  border-radius: 8px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
}

.quick-button:hover {
  background: #145c2b;
  color: white;
}

.typing-indicator {
  display: flex;
  gap: 0.3rem;
  padding: 0.2rem 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #666;
  border-radius: 50%;
  animation: typing 1s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

/* 스크롤바 스타일링 */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #999;
}
</style> 