<template>
  <div class="views-bmap">
    <div id="queries">
      <el-col :gutter="20">
        <el-col :span="6">
          <span>选择可以生成的图表:</span>
          <el-select v-model="modal.optional" id="option" placeholder="请选择" >
            <el-option v-for="item in bindings.optional" :key="item.value" :label="item.name" :value="item.value" > </el-option>
          </el-select>
        </el-col>
        <el-col :span="12">
          <el-input v-model="modal.desc" placeholder="请输入内容" ></el-input>
        </el-col>
      </el-col>
    </div>
    <div id="main"></div>
  </div>

</template>

<script>
var echarts = require("echarts");
var bmap = require("echarts/extension/bmap/bmap");
import { Elf } from "../modules/comm.js";
import { getRemarks } from "../modules/chart/bmap";
import { stockService } from "../modules/stockService";

export default {
  props: {},
  data() {
    return {
      dom: null,
      target: null,
      remarks: null,
      modal: {
        optional: "",
        desc: ""
      },
      bindings: {
        optional: []
      }
    };
  },
  created() {},
  mounted() {
    let self = this;
    self.dom = document.getElementById("main");
    self.remarks = getRemarks();
    self.init();
  },
  computed: {},
  methods: {
    getData: function() {
      stockService.getPoint().done(function(ret) {
        var d = [];
        var m = {};
        var stock_basic = {};
        $.each(ret.rows, function(oi, ov) {
          var position = ov.position;
          if (position && position.lng) {
            stock_basic = ov.stock_basic2o;
            m = stock_basic || {};
            m["introduction"] = ov.introduction || "";
            // console.log(""+ov.employees)
            m["employees"] = ov.employees || "";
            m["business_scope"] = ov.business_scope || "";
            m["main_business"] = ov.main_business || "";
            d.push([position.lng, position.lat, m]);
          }
        });
        return d;
      });
    },

    init: function() {
      // 可以理解未 初始化，
      let self = this;
      var comm = Elf.comm;
      var toSelect = comm.dictToArray(self.remarks);
      self.bindings.optional = toSelect.map(function(v, i) {
        // 默认书写为
        // var value = v.value.option || "option" + comm.toFirstUpperCase(v.key);
        if (v.value.default) {
          self.modal.optional =  v.key;
        }
        return {
          name: v.key,
          value: v.name|| v.key
        };
      });

       self.target = echarts.init(self.dom);
       self.render();
    },
    render: function() {
      let self = this;
      // 可以多次渲染

      var remark = self.remarks[self.modal.optional];

      self.modal.desc = remark.desc || "";
      var option = remark.setting;

      // self.getData()

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
.views-bmap {
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