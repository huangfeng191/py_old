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
      label="处理状态"
      width="80">
      <template slot-scope="scope"  >
        <span style="color:red">  {{scope.row.marked=='store'?"已收藏":scope.row.marked=='shield'?"已屏蔽":""}}</span>
      </template>
    </el-table-column>
        <el-table-column
      fixed="right"
      label="操作"
      width="100">
      <template slot-scope="scope">
        <el-button @click="handleClick(scope.row)" type="text" size="small" style="padding-left:10px">查看</el-button>
        <el-button @click="handleMark(scope.row,'store')" type="text" size="small">收藏</el-button>
        <el-button @click="handleMark(scope.row,'shield')" type="text" size="small">屏蔽</el-button>
        <el-button @click="handleMark(scope.row,'')" type="text" size="small">取消</el-button>
      </template>
    </el-table-column>


      </el-table>
    </div>

  </el-dialog>

</template>

<script>
import { CRUD } from "../../modules/service";
export default {
  props: {
      "detailList":{
         type:Array
          
      },
 
      
  },
  data() {
    return {
      dialogVisible:false,
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
        //  { title: "marked", field: "marked" },
        { title: "url", field: "url" ,width:"200"},
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
    init(){
      this.dialogVisible=true
    },
    handleMark(row,marked){
      let self=this;
      
        row["marked"]=marked
             let house = CRUD("nms", "house_mark");
        house
          .update(row)
          .done(function(v) {
           self.$emit("refresh")
          });
      
    },
      handleClick(row){
        var url=row.url.split("&now_time")[0]
          window.open(url)
          
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