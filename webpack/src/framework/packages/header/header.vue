<template>
    <div class="ff-header">
      <header :style="{height:headerHeight,width:headerWidth}">
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
    name: 'ffHeader',
    props: {
      headerHeight:{
        type:String,
        default:'100%'
      },
      headerWidth:{
        type:String,
        default:'100%'
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