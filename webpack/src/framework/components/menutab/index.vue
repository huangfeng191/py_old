<template>
  <div class="menutab-index">
    <div class="tabs">
      <template v-for="(item, index) in tabs">

        <template v-if="item.id==current.id">
          <div :data-index='index' :class="['menu-name','is-active',item.id]" :key="item.id">
            <span slot="label" class="showCurrent" @click="selectMenu(item.val,item.id)">
              <i class="el-icon-date"></i> {{item.nm}}</span>
            <span v-if='tabs.length>1' class="el-icon-close" @click="closeMenu(item.val,item.id)"></span>
          </div>

        </template>
        <template v-else>
          <div :data-index='index' :class="['menu-name',item.id]" :key="item.id">
            <span slot="label" class="showCurrent" @click="selectMenu(item.val,item.id)">
              <i class="el-icon-date"></i> {{item.nm}}</span>
            <span class="el-icon-close" @click="closeMenu(item.val,item.id)"></span>
          </div>
        </template>
      </template>

    </div>
    <div class="content">

      <div v-for="item in tabs" :key="item.id" :style="[item.id==current.id?{'height':'auto','overflow':'visible'}:{'height':'0','overflow':'hidden'}]">
        <iframe :src="item.val" width=100% :style="stl" frameborder="0" scrolling="no" allowfullscreen="true"></iframe>
      </div>

    </div>
  </div>

</template>

<script>
export default {
  props: {
    canotClose: false
  },
  data() {
    return {
      stl: "",
      val: "http://www.baidu.com",
      tabs: [
        { id: "1", val: "/stock/interfaceconfig.html", nm: "页面配置" },
        { id: "3", val: "/stock/admin.html", nm: "接口数据获取" },
        { id: "11", val: "/stock/interfacedata.html?table_nm=stock_basics", nm: "获取股票基本信息" },
        { id: "12", val: "/stock/interfacedata.html?table_nm=industry_classified", nm: "行业分类" },
        { id: "13", val: "/stock/interfacedata.html?table_nm=concept_classified", nm: "概念分类" },
        { id: "14", val: "/stock/interfacedata.html?table_nm=area_classified", nm: "地域分类" },
        { id: "61", val: "/out.html#/hdmenu", nm: "cs顶部menu" },
      ],
      current: {
        id: "1",
        val: ""
      }
    };
  },
  created() {},
  mounted() {
    debugger;
    var h = $(".menutab-index").height() - 40;
    this.stl = "width: 100%;height:" + h + "px";
  },
  computed: {},
  methods: {
    closeMenu(val, id) {
      let self = this;
      self.tabs = self.tabs.filter(function(v) {
        return v.id == id ? false : true;
      });

      self.current.id = self.tabs[self.tabs.length - 1].id;
      self.current.val = self.tabs[self.tabs.length - 1].val;
    },
    selectMenu(val, id) {
      let self = this;
      self.current.id = id;
      self.current.val = val;
    }
  },
  watch: {},
  components: {}
};
</script>
<style lang="less" >
@tabs-height: 36px;

.menutab-index {
  height: 100%;
  width: 100%;
  .tabs {
    height: @tabs-height;
    background-color: yellow;

    .menu-name {
      padding: 0 16px;
      height: 36px;
      box-sizing: border-box;
      line-height: 36px;
      list-style: none;
      font-size: 14px;
      color: #666;
      margin-bottom: -1px;
      position: relative;
      transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);
      border: 1px solid transparent;
      border-top: 0;
      margin-right: -1px;
      margin-left: -1px;
      display: inline-block;
      padding: 0 8px;
      background-color: #edf1f2;
      border-left-color: #fff;
      margin-bottom: 0;
      font-size: 12px !important;
      .el-icon-close {
        font-family: "element-icons" !important;
        font-style: normal;
        font-weight: 400;
        font-variant: normal;
        text-transform: none;
        line-height: 1;
        vertical-align: baseline;
        display: inline-block;
        -webkit-font-smoothing: antialiased;
        border-radius: 50%;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);
        margin-left: 5px;
        font-size: 12px;
      }
    }
    .menu-name.is-active {
      background-color: #fff;
      border-right-color: #d9d9d9;
      border-left-color: #d9d9d9;
      color: #666;
      background-color: #98dbf2;
    }
    .menu-name:hover span {
      color: #1f2d3d;
      cursor: pointer;
    }
    .menu-content {
      // display: block;
      // opacity: 0;
    }
    .select-menu-content {
      width: 100%;
    }
  }
  .content {
    width: 100%;
    height: calc(~"100%" - @tabs-height + 4px);
  }
}
</style>