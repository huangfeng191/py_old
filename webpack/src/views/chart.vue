<template>
  <div class="views-chart">
    <div id="queries">
      <span>选择可以生成的图表:</span>
      <select id="option">
      </select>
      <input id="desc">

    </div>
    <div id="main"></div>
  </div>

</template>

<script>
var echarts = require("echarts");
import { Elf } from "../modules/comm.js";
import { getRemarks } from "../modules/chart/normal";

export default {
  props: {},
  data() {
    return {
      dom: null,
      target: null,
      remarks:null
    };
  },
  created() {},
  mounted() {
    let self = this;
    self.dom = document.getElementById("main");
    self.remarks=getRemarks();
    self.init();
  },
  computed: {},
  methods: {
    init: function() {
      // 可以理解未 初始化，
      let self = this;
      var comm = Elf.comm;
      var toSelect = comm.dictToArray(self.remarks);
      var selectOption = toSelect.map(function(v, i) {
        // 默认书写为
        return {
          name: v.key,
          value: v.value.option || "option" + comm.toFirstUpperCase(v.key),
          default: v.value.default
        };
      });
      comm.setSelectOption($("#option"), selectOption);

      self.target = echarts.init(self.dom);
      self.render();

      $("#option").on("change", function() {
        self.render();
      });
    },
    render: function() {
      let self = this;
      // 可以多次渲染
      var typeDom = $("#option").val();

      var remark = self.remarks[$("#option :selected").html()];

      var desc = remark.desc;
      $("#desc").val(desc);
      var option = remark.setting;
      self.target.clear();
      self.target.setOption(option);
    }
  },
  watch: {},
  components: {}
};
</script>
<style lang="less" >
@offset-top: 200px;
.views-chart {
  width: 100%;
  height: 100%;
  #queries {
    width: 100%;
    height: calc(~"@{offset-top}");
    #desc {
      width: 400px;
    }
  }
  #main {
    width: 100%;
    height: calc(~"100% - @{offset-top}");
  }
}
</style>