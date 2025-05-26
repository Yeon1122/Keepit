import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SignupView from '@/views/SignupView.vue'
import LoginView from '@/views/LoginView.vue'
import SavingsView from '@/views/SavingsView.vue'
import MypageView from '@/views/MypageView.vue'
import UserEditView from '@/views/UserEditView.vue'
import FollowListView from '@/views/FollowListView.vue'
import UserDetailView from '@/views/UserDetailView.vue'
import StocksView from '@/views/StocksView.vue'
import StockDetailView from '@/views/StockDetailView.vue'
import GoodsView from '@/views/GoodsView.vue'
import SavingsCompareView from '@/views/SavingsCompareView.vue'
import FreeCommunityView from '@/views/FreeCommunityView.vue'
import FreePostCreateView from '@/views/FreePostCreateView.vue'
import FreePostDetailView from '@/views/FreePostDetailView.vue'
import FreePostEditView from '@/views/FreePostEditView.vue'
import MyPostsView from '@/views/MyPostsView.vue'
import InvestmentTestView from '@/views/InvestmentTestView.vue'
import TestResultView from '@/views/TestResultView.vue'
import LocationView from '../views/LocationView.vue'
import ChatbotView from '../views/ChatbotView.vue'
import MyFavoritesView from '@/views/MyFavoritesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/location',
      name: 'location',
      component: LocationView
    },
    {
      path: '/chatbot',
      name: 'chatbot',
      component: ChatbotView
    },
    {
      path: '/users/signup',
      name: 'signup',
      component: SignupView,
    },
    {
      path: '/users/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/products/savings',
      name: 'savings',
      component: SavingsView,
    },
    {
      path: '/users/mypage',
      name: 'mypage',
      component: MypageView,
    },
    {
      path: '/users/mypage/edit',
      name: 'useredit',
      component: UserEditView,
    },
    {
      path: '/users/follow/:userid',
      name: 'follow',
      component: FollowListView,
      meta: { requiresAuth: true }
    },
    {
      path: '/users/:userid',
      name: 'userpage',
      component: UserDetailView,
    },
    {
      path: '/products/stocketf',
      name: 'stocks',
      component: StocksView,
    },
    {
      path: '/products/stocks/:stock_code',
      name: 'stockdetail',
      component: StockDetailView,
    },
    {
      path: '/products/goods',
      name: 'goods',
      component: GoodsView,
    },
    {
      path: '/savings/compare',
      name: 'compare',
      component: SavingsCompareView,
    },
    {
      path: '/community/free',
      name: 'freecommunity',
      component: FreeCommunityView,
    },
    {
      path: '/community/free/create',
      name: 'freepostcreate',
      component: FreePostCreateView,
    },
    {
      path: '/community/free/:id',
      name: 'freepostdetail',
      component: FreePostDetailView,
    },
    {
      path: '/posts/free/:id/edit',
      name: 'freepostedit',
      component: FreePostEditView,
    },
    {
      path: '/question',
      name: 'questioncommunity',
      component: () => import('../views/QuestionCommunityView.vue')
    },
    {
      path: '/question/create',
      name: 'questioncreate',
      component: () => import('../views/QuestionPostCreateView.vue')
    },
    {
      path: '/question/:id',
      name: 'questiondetail',
      component: () => import('../views/QuestionPostDetailView.vue')
    },
    {
      path: '/question/:id/edit',
      name: 'questionedit',
      component: () => import('../views/QuestionPostEditView.vue')
    },
    {
      path: '/users/mypage/posts',
      name: 'myposts',
      component: MyPostsView
    },
    {
      path: '/test',
      name: 'investmenttest',
      component: InvestmentTestView,
      meta: { requiresAuth: true }
    },
    {
      path: '/test/result',
      name: 'testresult',
      component: TestResultView,
      meta: { requiresAuth: true }
    },
    {
      path: '/my/favorites',
      name: 'myfavorites',
      component: MyFavoritesView,
      meta: { requiresAuth: true }
    },
  ],
})

// 인증이 필요한 페이지 목록
const authRequiredPages = [
  'mypage',
  'useredit',
  'follow',
  'myposts',
  'investmenttest',
  'testresult',
  'freepostcreate',
  'freepostedit',
  'questioncreate',
  'questionedit',
  'compare',
  'myfavorites'
]

// 비로그인 상태에서만 접근 가능한 페이지
const guestOnlyPages = ['login', 'signup']

router.beforeEach((to, from, next) => {
  // localStorage의 account 정보에서 인증 상태 확인
  const accountData = JSON.parse(localStorage.getItem('account') || '{}')
  const isAuthenticated = !!accountData.token && accountData.isAuthenticated

  // 인증이 필요한 페이지에 접근하려는 경우
  if (authRequiredPages.includes(to.name) && !isAuthenticated) {
    alert('로그인이 필요한 서비스입니다.')
    next({
      name: 'login',
      query: { redirect: to.fullPath }
    })
    return
  }

  // 이미 로그인한 사용자가 로그인/회원가입 페이지에 접근하려는 경우
  if (guestOnlyPages.includes(to.name) && isAuthenticated) {
    alert('이미 로그인되어 있습니다.')
    next({ name: 'home' })
    return
  }

  next()
})

export default router