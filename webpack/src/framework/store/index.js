
import Vue from "vue"
import Vuex from "vuex"
Vue.use(Vuex)
require('../../../static/js/mh');
const state = {
    History:mh.History
}

const mutations = {

    addMenu(state, menu) {
        state.History.Pages.push($.extend({}, menu));
        state.History.Current = { Id: menu.Id, Item: $.extend({}, menu) };
    },

    selectMenu(state, menu) {
        state.History.Current = { Id: menu.Id, Item: $.extend({}, menu) };
        Open(menu.val);
       
    },

    removeMenu(state, menuId) {
        if (state.History.Pages.length > 1) {
            for (var i = 0; i < state.History.Pages.length; i++) {
                if (state.History.Pages[i].Id == menuId) {
                    state.History.Pages.splice(i, 1);
                    break;
                }
            }
            let menu=state.History.Pages[state.History.Pages.length - 1];
            window.App.$store.commit("selectMenu", menu);
          
            
        }
    },
}

export default new Vuex.Store({
    state,
    mutations
});