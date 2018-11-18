<template>
    <div class="comm-markdown">
        12
    </div>

</template>

<script>
import marked from "marked"
export default {
  props: {},
  data() {
    return {};
  },
  created() {},
  mounted() {
      debugger
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