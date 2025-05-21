<template>
    <div>
        <div class="middle-1">
            <div class="left">
                <div class="picture">
                    <img src="@/assets/images/Momo_test.png">
                </div>
            </div>
            <div class="right">
                <p class="subtitle">내 손 안의 금융비서</p>
                <p class="title">킵잇</p>
                <p class="explain">간단한 테스트로 나에게 맞는 투자 성향과 금융 상품을 추천해드려요. 나에게 꼭 맞는 금융 루틴, 지금 바로 시작해보세요!</p>
                <button class="go-to-test">투자 스타일 알아보기</button>
            </div>
        </div>
        <div class="middle-2">

        </div>

    </div>
</template>

<script setup>

</script>

<style scoped>
    .middle-1 {
    background-color: #f5f5f5;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 3rem 2rem;
    }

    .middle-1 > div {
    flex: 1;
    }

    .left {
    display: flex;
    justify-content: center; /* 수평 가운데 정렬 */
    align-items: center;     /* 수직 가운데 정렬 */
    }

    .picture img {
    width: 300px;
    max-width: 100%;
    height: auto;
    }

    .subtitle {
    font-size: 1.25rem;
    color: #1d4a2d;
    margin-bottom: 2rem;
    }

    .title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1d4a2d; /* 진한 초록 */
    margin-bottom: 0.1rem;
    }

    .explain {
    font-size: 1rem;
    line-height: 1.6;
    color: #333;
    margin-bottom: 0.75rem;
    }

    .go-to-test {
    background-color: #1d4a2d;
    color: white;
    border: none;
    padding: 0.8rem 1.5rem;
    font-size: 1rem;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
    }

    .go-to-test:hover {
    background-color: #145c2b;
    }

</style>