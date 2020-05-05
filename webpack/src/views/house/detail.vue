<template>
  <el-dialog 
  width="90%"
    :visible.sync="dialogVisible">

    <div class="house-detail">
      <el-table
        :data="detailList"
         height="550"
         border
        style="width: 100%;"
       
      >
        <el-table-column
          v-for="r in  colunms"
          :key="r.field"
          :prop="r.field"
          :label="r.title"
          :width="r.width||100"
        >
        </el-table-column>


        <el-table-column
      fixed="right"
      label="操作"
      width="100">
      <template slot-scope="scope">
        <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button>
      </template>
    </el-table-column>


      </el-table>
    </div>

  </el-dialog>

</template>

<script>
export default {
  props: {
      "detailList":{
         type:Array
          
      },
      "dialogVisible":{
           type:Boolean,
            default:false
          
      }
      
  },
  data() {
    return {
      colunms: [
     
        { title: "total_price", field: "total_price" },
        // { title: "total_price_unit", field: "total_price_unit" },
        { title: "avg_price", field: "avg_price" },
        { title: "avg_price_unit", field: "avg_price_unit" },
        { title: "title", field: "title" ,width:"200" },
        { title: "house_type", field: "house_type" },
        { title: "building_area", field: "building_area" },
        { title: "building_area_unit", field: "building_area_unit" },
        { title: "floor", field: "floor" },
        { title: "building_time", field: "building_time" },
        { title: "community", field: "community"  ,width:"120"},
        { title: "city", field: "city" },
        { title: "area", field: "area" },
        { title: "address", field: "address" },
        { title: "advantage", field: "advantage" },
        { title: "salesman", field: "salesman" },
        // { title: "url", field: "url" ,width:"200"},
        // { title: "url_md5", field: "url_md5" },
        { title: "create_time", field: "create_time" },
           { title: "id", field: "id" },
      ],
  
    };
  },
  created() {},
  mounted() {},
  computed: {},
  methods: {
      handleClick(row){
          window.open(row.url)
          debugger
      }
  },
  watch: {},
  components: {}
};
</script>
<style lang="less" >
.house-detail {
    .el-table__body-wrapper{
        height: 500px;
    }
}
</style>