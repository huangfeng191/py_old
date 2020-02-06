<template>
  <div class="menutab-index">
    <div class="Pages">
      <span v-for="(item, index) in Pages" :key="item.Id">

        <template v-if="item.Id==Current.Id">
          <div :data-index='index' :class="['menu-name','is-active',item.Id]" :key="item.Id">
            <span slot="label" class="showCurrent" @click="selectMenu(item.val,item.Id)">
              <i class="el-icon-date"></i> {{item.nm}}</span>
            <span v-if='Pages.length>1' class="el-icon-close" @click="closeMenu(item.val,item.Id)"></span>
          </div>

        </template>
        <template v-else>
          <div :data-index='index' :class="['menu-name',item.Id]" :key="item.Id">
            <span slot="label" class="showCurrent" @click="selectMenu(item.val,item.Id)">
              <i class="el-icon-date"></i> {{item.nm}}</span>
            <span class="el-icon-close" @click="closeMenu(item.val,item.Id)"></span>
          </div>
        </template>
      </span>

      <div class="other-wrap">

        <div class="command" title="刷新" @click="onRefresh">
          <span class="refresh">
            <i class="el-icon-refresh "></i>
          </span>
        </div>
      </div>

    </div>
    <div class="content">

      <div v-for="item in Pages" :key="item.Id" :style="[item.Id==Current.Id?{'height':'auto','overflow':'visible'}:{'height':'0','overflow':'hidden'}]">
        <iframe :src="item.val" :id="item.Id" width=100% :style="stl" frameborder="0" scrolling="no" allowfullscreen="true"></iframe>
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
      stl: ""
    };
  },
  created() {},
  mounted() {
    var h = $(".menutab-index").height() - 40;
    this.stl = "width: 100%;height:" + h + "px";
    let self=this;
    
        $(document).keydown(function (event) {
              if (event.key == "F2"){
                document.getElementById(self.$store.state.History.Current.Id).contentWindow.location.reload(true);
              }
            })


  },
  computed: {
    Pages: function() {
      return this.$store.state.History.Pages;
    },
    Current: function() {
      return this.$store.state.History.Current.Item;
    }
  },
  methods: {
    onRefresh() {
      document.getElementById(this.$store.state.History.Current.Id).contentWindow.location.reload(true);
    },

    closeMenu(val, Id) {
      let self = this;
      self.$store.commit("removeMenu", Id);
    },
    selectMenu(val, Id) {
      let self = this;
      let menu = self.Pages.find(page => {
        return page.Id == Id;
      });
      if (menu) {
        self.$store.commit("selectMenu", menu);
      }
    }
  },
  watch: {},
  components: {}
};
</script>
<style lang="less" >
@Pages-height: 36px;

.menutab-index {
  height: 100%;
  width: 100%;
  .Pages {
    height: @Pages-height;
    background-color: yellow;
    background-color: #0481c4;

    .other-wrap {
      float: right;
      right: 20px;
      top: 0;
      .refresh {
        color: #fff;
        font-size: 18px;
        line-height: 32px;
        display: inline-block;
        margin-right: 10px;
        cursor: pointer;
      }
    }

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
    height: calc(~"100%" - @Pages-height + 4px);
  }
}
</style>