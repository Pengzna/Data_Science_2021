<template>
  <div>

    <div class="background-card">


            <el-card :body-style="{ padding: '0px' }" class="card1">
              <img src="../assets/smile.png" class="image">
              <div style="padding: 14px;">
                <span class="intro1">自动化</span>
                <br>
                <br>
                <span class="intro2">爬取案例、文本分词、数据分析...</span>
              </div>
            </el-card>

      <el-card :body-style="{ padding: '0px' }" class="card2">
        <img src="../assets/lawHall.png" class="image">
        <div style="padding: 14px;">
          <span class="intro1">1000+</span>
          <br>
          <br>
          <span class="intro2">数据集训练模型与测试</span>
        </div>
      </el-card>

      <el-card :body-style="{ padding: '0px' }" class="card3">
        <img src="../assets/hall.png" class="image">
        <div style="padding: 14px;">
          <span class="intro1">反馈学习</span>
          <br>
          <br>
          <span class="intro2">利用数据分析算法提高标注效率</span>
        </div>
      </el-card>

    </div>

    <div style="background:linear-gradient(to left,#FFFFFF,#b6b6b6,#FFFFFF);
    height:3px;
    position: relative;
    margin-top: 30px"></div>

  </div>
</template>

<script>
export default {
  name: "cardBody"
}
</script>

<style scoped>

  .background-card{
    position: relative;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    background-color: #F5F9FC;
    height: 250px;
    width: 74%;
    margin-top: 30px;
    margin-left: 13%;
  }

  .card1{
    position: absolute;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
    background-color: #FFFFFF;
    height: 73%;
    width: 30%;
    top:15%;
    left:2%;
    z-index: 1;
  }
  .card2{
    position: absolute;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
    background-color: #FFFFFF;
    height: 73%;
    width: 30%;
    top:15%;
    left:35%;
    z-index: 1;
  }
  .card3{
    position: absolute;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
    background-color: #FFFFFF;
    height: 73%;
    width: 30%;
    top:15%;
    left:68%;
    z-index: 1;
  }

  .intro1{
    font-family: "思源宋体 CN Heavy";
    font-size: xx-large;
    color: #1D5C93;

  }

  .intro2{
    font-family: "方正苏新诗柳楷简体";
    font-size: medium;
    color: #2C3E50;
  }

  .image {
    width: 20%;
    margin-left: 40%;
    margin-top: 4%;;
    display: block;
  }

</style>

