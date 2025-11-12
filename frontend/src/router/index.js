import { createRouter, createWebHashHistory } from "vue-router"
import Stream from '../components/Stream.vue'
import View from '../components/View.vue'

const routes = [
  {
    path: "/",
    name: "Stream",
    component: Stream
  },
  {
    path: '/view/:playbackId',
    component: View
  }
]

const router = createRouter({
  history: createWebHashHistory("/vue_live_player/"),
  routes
})

export default router
