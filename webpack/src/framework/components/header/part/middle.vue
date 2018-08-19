<template>
    <div class="header-part-middle">
        <div class="app-list">
            <div class="el-submenu__title" :class="[actV==i?'is-active':'']" v-for="(menu1,i) in SingleMenu" :key="menu1.sn" @click="appSelect(i)">
                <i :class='menu1.style||"iconfont icon-setting"' style="font-size: 38px; position: absolute; top: -18px; right: 10px;"></i>
                <span style=" display: inline-block; margin-right: 3px; position: relative; right: 16px; bottom: -4px; font-size: 12px; ">{{menu1.name}}</span>

            </div>
        </div>
    </div>

</template>

<script>
export default {
  props: {},
  data() {
    return {
      actV: 0
    };
  },
  created() {},
  mounted() {},
  computed: {
    SingleMenu: function() {
      //   return this.$store.state.Menus.Children;
      // {sn  style name}
      return [
          { sn: 1, style: null, name: "页面维护" },
          { sn: 2, style: null, name: "配置页面" }
          ];
    }
  },
  methods: {
    appSelect(index) {
      debugger;
      if (index != this.actV) {
        this.actV = index;
      }
    }
  },
  watch: {},
  components: {}
};
</script>
<style lang="less" >
@header-height: 80px;

.header-part-middle {
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
  }
}
</style>