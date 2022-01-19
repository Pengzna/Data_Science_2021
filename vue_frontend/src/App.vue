<template>
  <div id="app">
    <div>
      <head-title style="position: fixed; top: 0; z-index: 4"></head-title>
    </div>

    <div>
      <text-title style="margin-top: 100px;"></text-title>
    </div>

    <div>
      <card-body></card-body>
    </div>

    <div>
      <main-body style="margin-bottom: 100px"></main-body>
    </div>

    <div>
      <end-title style="position: fixed; bottom: -15px; z-index: 4"></end-title>
    </div>
  </div>
</template>

<script>
import headTitle from "@/components/headTitle";
import textTitle from "@/components/textTitle";
import cardBody from "@/components/cardBody";
import mainBody from "@/components/mainBody";
import endTitle from "@/components/endTitle";

export default {
  name: 'App',
  components: {
    headTitle,
    textTitle,
    cardBody,
    mainBody,
    endTitle,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif, 方正苏新诗柳楷简体;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
