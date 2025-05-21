<template>
    <div>
        <Header/>

        <main class="main-content">
            <RouterView />
        </main>

        <Footer/>


    </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

</script>

<style scoped>

</style>