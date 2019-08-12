<template>
  <div id="app">
    <!-- <div style="height:25px;">
            <router-link to="/cs_js">cs_js</router-link>
            <router-link to="/hmenu">hmenu</router-link>
            <router-link to="/markdown">markdown</router-link>
        </div> -->
    <router-view></router-view>
  </div>
</template>
<script>
export default {
  name: "app",
  props: ["sss"],
  data() {
    return {
      msg: "Welcome to Your Vue.js App",
      cs: "app_"
    };
  }
};
</script>

<style lang="less" >
html {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  body {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    #app {
      width: 100%;
      height: 100%;
      margin: 0;
      padding: 0;
    }
  }
}
</style>
