<template>
  <div class="head-menu">
    <div class="app-list">
      <div class="el-submenu__title" style="position:relative;" :class="[actV==i?'is-active':'']" v-for="(menu1,i) in SingleMenu" :key="menu1.sn">
        <div @mouseenter="appSelect(i)" @click="initPages(menu1)">
          <i :class='menu1.style||"iconfont icon-setting"' style="font-size: 38px; position: absolute; top: -18px; right: 10px;"></i>
          <span style=" display: inline-block; margin-right: 3px; position: relative; right: 16px; bottom: -4px; font-size: 12px; ">{{menu1.nm}}</span>
        </div>
        <div v-if="actShow==i" @mouseleave="appSelect(i)" style="position:absolute;z-index:100" :style="{width:((menu1.Children.length)*140+30)+'px'}">
          <el-row style="margin-left:10px;">
            <div class="menu-list" style="display:inline-block;box-sizing:border-box;vertical-align: top;" v-for="child in menu1.Children" :key="child.sn">
              <p style="width:140px;word-wrap:normal;font-size:15px; padding-bottom:10px;    line-height: 20px; margin: 0;">{{child.nm}}</p>
              <i style="font-size:14px;line-height:24px; display:block;font-style:normal;" v-for="c1 in child.Children" :key="c1.sn">
                <span class="pointer" @click="openUrl(c1.val)" style="color: rgb(102, 102, 102)">
                  {{c1.nm}}
                </span>
              </i>
            </div>
          </el-row>
        </div>
      </div>

    </div>
  </div>

</template>

<script>
export default {
  props: {},
  data() {
    return {
      actV: 0,
      actShow: -1
    };
  },
  created() {},
  mounted() {},
  computed: {
    SingleMenu: function() {
      //   return this.$store.state.Menus.Children;
      // {sn  style nm}
      return window.mh.Menus;
    }
  },
  methods: {
    openUrl(url) {
      Open(url);
    },
    initPages(menu) {
      mh.History.Pages = [];
      mh.History.Current = {};
      function getChildren(menus) {
        $.each(menus, function(mi, mv) {
          if (mv.val) {
            if (mv.open) {
              mh.History.Pages.push(mv);
              mh.History.Current = { Id: mv.Id, Item: mv };
            }
          }
          if (mv.Children && mv.Children.length > 0) {
            getChildren(mv.Children);
          }
        });
      }
      getChildren(menu.Children);
    },
    appSelect(index) {
      if (index != this.actV) {
        this.actV = index;
        this.actShow = index;
      } else {
        if (this.actShow == -1) {
          this.actShow = index;
        } else {
          this.actShow = -1;
        }
      }
    }
  },
  watch: {},
  components: {}
};
</script>
<style lang="less" >
@header-height: 80px;

.head-menu {
  padding-left: 15px;
  .app-list {
    padding-top: 10px;
    .el-submenu__title {
      line-height: @header-height;
      float: left;
      color: #eeeeee;
      width: 58px;
      height: 58px;
      margin-right: 10px;
      border-radius: 5px;
      border: solid 1px #6293bf;

      &.is-active {
        background-color: #b57a48;
        color: #eeeeee;
      }
      &:hover {
        background-color: #b57a48;
        color: #eeeeee;
      }
    }
    .menu-list {
      background-color: #0290da;
      color: white;
      margin: -20px 0 0 -28px;
      padding-top: 10px;
      padding-left: 10px;
      padding-bottom: 10px;
    }
  }
}
</style>