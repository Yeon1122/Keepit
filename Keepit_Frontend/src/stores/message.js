import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useMessageStore = defineStore('message', () => {
    const message = ref('')
    const type = ref('') // 'success' | 'error' | 'info' | 'warning'
    const isVisible = ref(false)
    const timeout = ref(null)

    const showMessage = (text, messageType = 'info') => {
        message.value = text
        type.value = messageType
        isVisible.value = true

        // 이전 타이머가 있다면 제거
        if (timeout.value) {
            clearTimeout(timeout.value)
        }

        // 3초 후 메시지 숨기기
        timeout.value = setTimeout(() => {
            isVisible.value = false
        }, 3000)
    }

    const hideMessage = () => {
        isVisible.value = false
        if (timeout.value) {
            clearTimeout(timeout.value)
        }
    }

    return {
        message,
        type,
        isVisible,
        showMessage,
        hideMessage
    }
}) 