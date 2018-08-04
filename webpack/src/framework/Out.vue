<template>
    <div id="out">
        <div class="head">
            <a>跳转</a>
        </div>

        <section class="contant">
            <div class="menu"></div>
            <div class="detail">
                112121
            </div>
            <!--       <iframe src="part.html#anchor_1" width="100%" height="100%"></iframe> -->

        </section>

    </div>
</template>
<script>
export default {
  name: "out",
  props: [],
  data() {
    return {};
  }
};
</script>
<style lang="less">
#out {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0px;
  background-color: turquoise;
  .head {
    background-color: yellow;
    height: 50px;
    width: 100%;
  }
  .contant {
    height: calc(100% - 50px);
    width: 100%;
    .menu {
      width: 200px;
      height: 100%;
      float: left;
      background-color: gray;
    }
    .detail {
      width: calc(100% - 200px);
      height: 100%;
      float: left;
      background-color: burlywood;
    }
  }
}
</style>
