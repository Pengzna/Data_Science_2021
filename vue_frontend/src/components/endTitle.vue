<template>
  <el-footer style="background-color: #587187;width: 100%; height: 40px; margin-left:-10px">
    <div>
    <div class="text1">©Copyright</div>
    <div class="text2">Zhoubin Zheng, Xinyi Liu, Junzhi Peng.</div>
    <div class="text3">All Rights Reserved</div>
  </div>
  </el-footer>

</template>

<script>
export default {
  name: "tail"
}
</script>

<style scoped>
  .text1{
    position: absolute;
    z-index: 2;
    font-family: "Adobe Arabic";
    font-size: x-large;
    font-weight: bold;
    color: #C9CFC9;
    margin-left: 27%;
    margin-top: 10px;
  }
  .text2{
    position: absolute;
    z-index: 2;
    font-family: "思源宋体 CN Heavy";
    font-size: large;
    font-weight: bold;
    color: #F8F8F8;
    margin-left: 35%;
    margin-top: 8px
  }
  .text3{
    position: absolute;
    z-index: 2;
    font-family: "Adobe Arabic";
    font-size: x-large;
    font-weight: bold;
    color: #C9CFC9;
    margin-left: 63%;
    margin-top: 10px;
  }
</style>
