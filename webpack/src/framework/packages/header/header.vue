<template>
    <div class="hd-header">
      <header :style="{height:headerHeight,width:headerWidth,background:headerBackground}">
        <div class="left">
          <slot name="left"></slot>
        </div>
        <div class="middle">
          <slot name="middle"></slot>
        </div>
        <div class="right">
          <slot name="right" ></slot>
        </div>
      </header>
    </div>
</template>
<script type="text/babel">
  export default {
    name: 'HdHeader',
    props: {
      headerHeight:{
        type:String,
        default:'50px'
      },
      headerWidth:{
        type:String,
        default:'100%'
      },
      headerBackground:{
        type:String,
        default:'rgb(43, 46, 54)'
      }
    },
    data () {
      return {
      };
    },
    methods: {
      
    },
    computed: {
    },
    mounted(){
      
    }
  };
</script>