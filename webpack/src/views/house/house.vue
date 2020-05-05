<template>
  <div class="house-house">
    <div id="main"></div>
  </div>

</template>

<script>
var echarts = require("echarts");
var bmap = require("echarts/extension/bmap/bmap");
import { CRUD } from "../../modules/service";
import set from "./set.js"
export default {
  props: {},
  data() {
    return {
      dom: "",
      target: ""
    };
  },
  created() {},
  mounted() {
    let self = this;
    debugger
    self.dom = document.getElementById("main");
    self.init();
  },
  computed: {},
  methods: {
    init() {
        let self=this;
        let option=set
      self.target = echarts.init(self.dom);
      let house=CRUD("nms","house")
      house.query({size:999}).done(function(v){
        
        let data= v.rows.map(function(one){
            let a=[one.location.lng,one.location.lat]
            a.push(one.avg)
            a.push(one)
            return a 
        })
        option["series"][0].data=data
         self.target.setOption(option);
    })
     
    }
  },
  watch: {},
  components: {}
};
</script>
<style lang="less" >
@offset-top: 10px;
.house-house {
  width: 100%;
  height: 100%;

  #main {
    width: 100%;
    height: calc(~"100% - @{offset-top}");
  }
}
</style>