import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SignupView from '@/views/SignupView.vue'
import LoginView from '@/views/LoginView.vue'
import SavingsView from '@/views/SavingsView.vue'
import MypageView from '@/views/MypageView.vue'
import UsereditView from '@/views/UsereditView.vue'
import FollowlistView from '@/views/FollowlistView.vue'
import OtheruserpageView from '@/views/OtheruserpageView.vue'

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
      path: '/users/follow',
      name: 'followlist',
      component: FollowlistView,
    },
    {
      path: '/users/:userid',
      name: 'userpage',
      component: OtheruserpageView,
    }
  ],
})

export default router