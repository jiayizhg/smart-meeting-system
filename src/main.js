import Vue from 'vue/dist/vue.js'
import App from './App.vue'
import router from "./router"
import store from './store'
import './assets/styles/main.css'
import Axios from 'axios'


Vue.config.productionTip = false



Vue.prototype.$axios = Axios
Axios.defaults.baseURL = '/scheduling'


new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')

