import Vue from 'vue/dist/vue.js'
import VueRouter from "vue-router"
import HelloWorld from '../components/HelloWorld.vue'
import scheduling from '../views/calendar/scheduling.vue'

Vue.use(VueRouter)

// const HelloWorld = { template: '<div>HelloWorld</div>' }
// const scheduling = { template: '<div>scheduling</div>' }

const routes = [
    {
        path: "/",
        name: "HelloWorld",
        component: HelloWorld,
    },
    {
        path: "/scheduling",
        name: "scheduling",
        component: scheduling,
    }
]

const router = new VueRouter({
    routes // short for `routes: routes`
  })

export default router