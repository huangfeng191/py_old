<template>
      <div class="herder-index">
         <ff-herder>
             <head-middle slot="middle"></head-middle>
         </ff-herder>
      </div>
       
</template>

<script>
import ffHerder from "../../packages/header/header.vue"
import headMiddle from "./part/middle.vue"
export default {
  props: {},
  data(){
    return {
    }
  },
  created() {},
  mounted() {},
  computed:{},
  methods: {},
  watch: {},
  components:{
      ffHerder,
      headMiddle
  }
};
</script>
<style lang="less" >
@header-bgcolor: #0290da;
.herder-index{
  height: 100%;
  background-color: @header-bgcolor;
}
</style>