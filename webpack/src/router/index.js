import Vue from 'vue'
import Router from 'vue-router'
import routerConfig from './config.js'
import commConfig from "./comm.js"
Vue.use(Router);

let route_o={
    routes:[]
};
route_o["routes"]=routerConfig.routes.concat(commConfig.routes);

export default new Router(route_o)





