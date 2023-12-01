import Vue from 'vue/dist/vue.js'
import App from './App.vue'
import router from "./router"
import './assets/styles/main.css'
import Axios from 'axios'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import { createPinia } from 'pinia'


// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { fas } from '@fortawesome/free-solid-svg-icons'

import 'devextreme/dist/css/dx.light.css';

/* add icons to the library */
library.add(fas)

/* add font awesome icon component */
Vue.component('font-awesome-icon', FontAwesomeIcon)

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.use(createPinia())

Vue.config.productionTip = false

// Vue.component(ClientOnly.name, ClientOnly)

Vue.prototype.$axios = Axios
Axios.defaults.baseURL = '/scheduling'


new Vue({
  router,
  render: h => h(App),
}).$mount('#app')

