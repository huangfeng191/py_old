<template>
    <div id="app">
        <div style="height:25px;">
            <router-link to="/cs_js">cs_js</router-link>
        </div>
        <router-view></router-view>
    </div>
</template>
<script>
export default {
    name: 'app',
    props: [
        "sss"
    ],
    data() {
        return {
            msg: 'Welcome to Your Vue.js App',
            "cs": "app_"
        }
    }
}
</script>
