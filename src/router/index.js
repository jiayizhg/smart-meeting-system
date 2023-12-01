import Vue from 'vue/dist/vue.js'
import VueRouter from "vue-router"
import HelloWorld from '../components/HelloWorld.vue'
import scheduling from '../views/calendar/scheduling.vue'
import Home from '../components/home.vue'
// import calendar from '../components/calendar.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
    },
    {
        path: "/HelloWorld",
        name: "HelloWorld",
        component: HelloWorld,
    },
    {
        path: "/scheduling",
        name: "scheduling",
        component: scheduling,
    },
    // {
    //     path: "/calendar",
    //     name: "calendar",
    //     component: calendar,
    // }
]

const router = new VueRouter({
    routes // short for `routes: routes`
  })

export default router