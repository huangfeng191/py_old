<template>
  <div class="views-bMap">
    <div id="queries"></div>
    <div id="main"></div>
  </div>

</template>

<script>
var echarts = require("echarts");

export default {
  props: {},
  data() {
    return {};
  },
  created() {},
  mounted() {
    var myChart = echarts.init(document.getElementById("main"));

    myChart.setOption({
      title: {
        text: "ECharts 入门示例"
      },
      tooltip: {},
      xAxis: {
        data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
      },
      yAxis: {},
      series: [
        {
          name: "销量",
          type: "bar",
          data: [5, 20, 36, 10, 10, 20]
        }
      ]
    });
  },
  computed: {},
  methods: {},
  watch: {},
  components: {}
};
</script>
<style lang="less" >
@offset-top: 200px;
.views-bMap {
  width:100%;
  height:100%;
  #queries{
     width: 100%;
    height: calc(~"@{offset-top}");
  }
  #main {
    width: 100%;
    height: calc(~"100% - @{offset-top}");
  }
}
</style>