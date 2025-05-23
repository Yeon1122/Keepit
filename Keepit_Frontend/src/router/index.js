import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SignupView from '@/views/SignupView.vue'
import LoginView from '@/views/LoginView.vue'
import SavingsView from '@/views/SavingsView.vue'
import MypageView from '@/views/MypageView.vue'
import UsereditView from '@/views/UsereditView.vue'
import FollowlistView from '@/views/FollowlistView.vue'
import OtheruserpageView from '@/views/OtheruserpageView.vue'
import StocksView from '@/views/StocksView.vue'
import StockdetailView from '@/views/StockdetailView.vue'
import GoodsView from '@/views/GoodsView.vue'
import SavingscompareView from '@/views/SavingscompareView.vue'
import FreecommunityView from '@/views/FreecommunityView.vue'
import FreepostcreateView from '@/views/FreepostcreateView.vue'
import FreepostdetailView from '@/views/FreepostdetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
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
      component: UsereditView,
    },
    {
      path: '/users/follow/:userid',
      name: 'followlist',
      component: FollowlistView,
    },
    {
      path: '/users/:userid',
      name: 'userpage',
      component: OtheruserpageView,
    },
    {
      path: '/products/stocketf',
      name: 'stocks',
      component: StocksView,
    },
    {
      path: '/products/stocks/:stock_code',
      name: 'stockdetail',
      component: StockdetailView,
    },
    {
      path: '/products/goods',
      name: 'goods',
      component: GoodsView,
    },
    {
      path: '/savings/compare',
      name: 'compare',
      component: SavingscompareView,
    },
    {
      path: '/community/free',
      name: 'freecommunity',
      component: FreecommunityView,
    },
    {
      path: '/community/free/create',
      name: 'freepostcreate',
      component: FreepostcreateView,
    },
    {
      path: '/community/free/:id',
      name: 'freepostdetail',
      component: FreepostdetailView,
    }
  ],
})

export default router