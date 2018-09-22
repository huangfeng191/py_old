<template>
  <div class="head-menu">
    <div class="app-list">
      <div class="el-submenu__title" style="position:relative;" :class="[actV==i?'is-active':'']" v-for="(menu1,i) in SingleMenu" :key="menu1.sn">
        <div @click="appSelect(i)">
          <i :class='menu1.style||"iconfont icon-setting"' style="font-size: 38px; position: absolute; top: -18px; right: 10px;"></i>
          <span style=" display: inline-block; margin-right: 3px; position: relative; right: 16px; bottom: -4px; font-size: 12px; ">{{menu1.name}}</span>
        </div>
        <div v-if="actShow==i" style="position:absolute;z-index:100" :style="{width:((menu1.Children.length)*120+30)+'px'}">
          <el-row style="margin-left:10px;">
            <div class="menu-list" style="display:inline-block;box-sizing:border-box;vertical-align: top;" v-for="child in menu1.Children" :key="child.sn">
              <p style="width:110px;word-wrap:normal;font-size:16px;     line-height: 20px; margin: 0;">{{child.name}}</p>
              <i style="font-size:14px;line-height:18px; display:block;" v-for="c1 in child.Children" :key="c1.sn">
                <span class="pointer" @click="openUrl(c1.val)" style="color: black;">
                  {{c1.name}}
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
      // {sn  style name}
      return [
        {
          sn: 1,
          style: null,
          name: "页面维护",
          Children: [
            {
              sn: 11,
              name: "12",
              Children: [
                { sn: 111, name: 111, val: "http://www.baidu.com" },
                { sn: 111, name: 111, val: "http://www.baidu.com" },
                { sn: 111, name: 111, val: "http://www.baidu.com" },
                { sn: 111, name: 111, val: "http://www.baidu.com" }
              ]
            }
          ]
        },
        {
          sn: 2,
          style: null,
          name: "配置页面",
          Children: [
            {
              sn: 11,
              name: "34",
              Children: [
                { sn: 111, name: 22, val: "http://www.baidu.com" },
                { sn: 111, name: 222, val: "http://www.baidu.com" },
                { sn: 111, name: 222, val: "http://www.baidu.com" },
                { sn: 111, name: 222, val: "http://www.baidu.com" }
              ]
            }
          ]
        }
      ];
    }
  },
  methods: {
    openUrl(url) {
      Open(url);
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