
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import router from './router'
import $ from 'jquery';

Vue.use(ElementUI)  

new Vue({
  router,
  el: '#app',
  data() {
    return {
       msg: 'Welcome to Your Vue.js App',
      "sss": "main_"
    }
  },

    /**
  template: '<App/>',
  components: { App }
  与  render: h => h(App) 写法相同
 */
  template: "<App :sss='sss'/>",
  components: { App }
})
