<template>
    <div class="comm-markdown">
        12
    </div>

</template>

<script>
import marked from "marked"
import {API} from "../modules/service.js"
export default {
  props: {},
  data() {
    return {};
  },
  created() {},
  mounted() {
      
    API.getStaticMd().done(function(x){
        
    })

    $.get("/static/md/stock/index.md", function(response, status, xhr) {
      $(".comm-markdown").html(marked(response));
    });
  },
  computed: {},
  methods: {},
  watch: {},
  components: {}
};
</script>
<style lang="less" >
.comm-markdown {
}
</style>