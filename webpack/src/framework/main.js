
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
import Out from './Out.vue'
import router from './router'
import $ from 'jquery';
Vue.use(ElementUI) 
require("../../static/css/layout.less") 
require('../../static/fonts/iconfont.css');
debugger
new Vue({
  router,
  el: '#out',
  data() {
    return {
       msg: 'Welcome to Your Vue.js Out',
      "sss": "main_"
    }
  },

    /**
  template: '<Out/>',
  components: { Out }
  与  render: h => h(Out) 写法相同
 */
  template: "<Out/>",
  components: { Out }
})
