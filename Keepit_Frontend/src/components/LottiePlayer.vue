<template>
  <div ref="container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import lottie from 'lottie-web'

const props = defineProps({
  animationData: {
    type: Object,
    required: true
  },
  loop: {
    type: Boolean,
    default: true
  },
  autoplay: {
    type: Boolean,
    default: true
  }
})

const container = ref(null)
let animation = null

onMounted(() => {
  if (container.value) {
    animation = lottie.loadAnimation({
      container: container.value,
      renderer: 'svg',
      loop: props.loop,
      autoplay: props.autoplay,
      animationData: props.animationData
    })
  }
})

onUnmounted(() => {
  if (animation) {
    animation.destroy()
  }
})

watch(() => props.animationData, (newData) => {
  if (animation) {
    animation.destroy()
  }
  if (container.value) {
    animation = lottie.loadAnimation({
      container: container.value,
      renderer: 'svg',
      loop: props.loop,
      autoplay: props.autoplay,
      animationData: newData
    })
  }
}, { deep: true })
</script> 