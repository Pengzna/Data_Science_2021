<template>
  <div style="position: relative ; top: 0; width: 100%; margin-left:-10px">
    <div style="background-color: #F8F8F8;width: 100%; height: 60px;">
      <div class="text1">Foundations of Data Science</div>
      <div class="text2">南京大学软件学院</div>
      <div class="text3">2021年秋</div>
    </div>

<!--    <div class="title">司法大数据自动化标注与分析</div>-->
<!--    <div class="text4">基于Selenium自动化爬虫、hanlp、PCA、反馈学习、机器学习、朴素贝叶斯等技术</div>-->
  </div>
</template>

<script>
export default {
  name: "head"
}
</script>

<style scoped>
    .text1{
      position: absolute;
      z-index: 2;
      font-family: "Adobe Arabic";
      font-size: xx-large;
      font-weight: bold;
      color: #628EB6;
      margin-left: 3%;
      margin-top: 12px;
    }
    .text2{
      position: absolute;
      z-index: 2;
      font-family: "思源宋体 CN Heavy";
      font-size: x-large;
      font-weight: lighter;
      color: #628EB6;
      margin-left: 70%;
      margin-top: 10px
    }
    .text3{
      position: absolute;
      z-index: 2;
      font-family: "思源宋体 CN Heavy";
      font-size: x-large;
      font-weight: lighter;
      color: #628EB6;
      margin-left: 85%;
      margin-top: 10px
    }
    .title{
      font-family: "思源宋体 CN Heavy";
      font-size: xx-large;
      color: #5E778E;
      margin-top: 40px;
    }
    .text4{
      margin-top: 10px;
      font-family: 方正苏新诗柳楷简体;
      font-weight: bold;
      font-size: large;
    }
</style>
