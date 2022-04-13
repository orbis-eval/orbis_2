import { createRouter, createWebHistory } from 'vue-router'
import AnnotationView from '../views/AnnotationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'annotaion', component: AnnotationView },

    // route level code-splitting
    // this generates a separate chunk (About.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    // { path: '/about', name: 'about', component: () => import('../views/AboutView.vue') },

    { path: '/:pathMatch(.*)*', redirect: '/' }
  ]
})

export default router
