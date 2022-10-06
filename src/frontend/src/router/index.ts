import { createRouter, createWebHistory } from 'vue-router'
import AnnotationView from '../views/AnnotationView.vue'
import CorporaListView from '../views/CorporaListView.vue'
import CorpusView from '../views/CorpusView.vue'
import DocumentView from '../views/DocumentView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'annotaion', component: AnnotationView },
    { path: '/corpora', name: 'corporalist', component: CorporaListView },
    { path: '/corpora/:corpus_name', name: 'corpus', component: CorpusView },
    { path: '/documents/:corpus_name/:da_id', name: 'document', component: DocumentView },

    { path: '/:pathMatch(.*)*', redirect: '/' }
  ]
})

export default router
