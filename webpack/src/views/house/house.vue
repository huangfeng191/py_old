<template>
  <div class="house-house">
    <div id="main"></div>
    <house-detail
      ref="houseDetail"
      @refresh="init"
      :detailList="detailList"
    ></house-detail>
  </div>

</template>

<script>
var echarts = require("echarts");
var bmap = require("echarts/extension/bmap/bmap");
import { CRUD } from "../../modules/service";
import set from "./set.js";
import HouseDetail from "./detail.vue";
export default {
  props: {},
  data() {
    return {
      conditions:[],
      query: {},
      detailList: [],

      dom: "",
      target: ""
    };
  },
  created() {},
  mounted() {
    let self = this;
    self.dom = document.getElementById("main");
    
  
    self.target = echarts.init(self.dom);
    self.target.on("click", function(params) {
      if (params.componentSubType == "effectScatter") {
        let d = params.data[3];
        let house = CRUD("nms", "house");
        house
          .post("list", {
            record: {
              community: d.address,
              conditions: self.conditions
            }
          })
          .done(function(v) {
            self.detailList = v.rows;
            self.$refs.houseDetail.init();
          });
      }
    });
   
    self.init();
  },
  computed: {},
  methods: {

    parseConditions() {
      let self = this;
      let query = this.$route.query
      self.query = query;
      let conditions = [];
      debugger
      Object.keys(query).forEach(function(k) {
        let condition = {
          Field: "",
          Value: "",
          Group: 1,
          Operate: "=",
          Relation: "and"
        };
        condition["Value"] = query[k];
        if(!condition["Value"]){
          return 
        }
        if (k.includes("_start")) {
          condition["Operate"] = ">=";
          condition["Field"] = k.replace("_start", "");
        } else if (k.includes("_end")) {
          condition["Operate"] = "<=";
          condition["Field"] = k.replace("_end", "");
        } else {
          condition["Field"] = k;
        }
        if (["building_area", "avg_price"].includes(condition["Field"])) {
          condition["Value"] = Number(condition["Value"]);
        }
        if(["marked"].includes(condition["Field"])){
            condition["Value"]=condition["Value"].split(",")
        }
        conditions.push(condition)
      });
      self.conditions=conditions
     
    },
    init() {
      let self = this;
      self.parseConditions()
      let option = set;

      let house = CRUD("nms", "house");
      house
        .query({
          size: 999,
          conditions: self.conditions
        })
        .done(function(v) {
          let data = v.rows.map(function(one) {
            let a = [one.location.lng, one.location.lat];
            a.push(one.avg);
            a.push(one);
            return a;
          });
          option["series"][0].data = data;
          self.target.setOption(option);
        });
    }
  },
  watch: {
    $route(to, from) {
     this.init()
    }
  },
  components: {
    HouseDetail
  }
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