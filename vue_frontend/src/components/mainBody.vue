<template>
 <div>

<!--   爬虫时间选择栏-->
   <fieldset class="spider-intro">
     选择案件时间进行自动化爬取
   </fieldset>

   <div class="block">
     <el-date-picker
         style="margin-top: 10px"
         v-model="timeValue"
         type="daterange"
         start-placeholder="开始日期"
         end-placeholder="结束日期"
         :default-time="['00:00:00', '23:59:59']">
     </el-date-picker>
     <el-button id="spider" type="primary" @click="onSpider">爬取案件</el-button>
   </div>

<!--   <span>点击上传：</span><input type="file" id="files1" @change="uploadFile1()">-->

   <fieldset class="text-intro">
     <legend>案件信息</legend>
     <legend>键入或选择爬取的案件txt文件</legend>
   </fieldset>
<!--   案件文件上传表单-->
   <div class="test">
        <el-form style="width: 75%" ref="form"  id="caseText" label-width="80px">
          <el-form-item style="margin-left: -18%;" >
            <el-input
                style="width: 100%;
                margin-top:20px"
                :rows="9"
                type="textarea"
                v-model="textValue">{{textValue}}
            </el-input>
          </el-form-item>
        </el-form>
   </div>

   <div class="button-group">
     <el-upload action="https://jsonplaceholder.typicode.com/posts/"
                class="upload-demo"
                :auto-upload="false"
                :on-change="openFile">
       <el-button style="margin-left: 0px" size="small" type="primary">上传案例文件</el-button>
     </el-upload>
     <el-button class="splitword-button" size="small" type="primary" @click="splitText">点击开始分词</el-button>
   </div>


<!--   -->
   <fieldset class="text-intro2">
     <legend>分词结果</legend>
     <legend>点击可选项，对信息进行标注</legend>
   </fieldset>

<!--   分类进行标注-->
   <el-tabs class="tag" type="border-card">
     <el-tab-pane label="当事人">
       <div style="text-align: left" v-for="(item, word, index) of tag" :key="index">
<!--            span里是词性标题-->
         <span class="tagTitle" v-if="word === 'noun'">名词</span>
         <span class="tagTitle" v-if="word === 'verb'">动词</span>
         <span class="tagTitle" v-if="word === 'adjectives'">形容词</span>
         <span class="tagTitle" v-if="word === 'adverb'">副词</span>
<!--            下面是复选框-->
            <el-checkbox-group style="margin-bottom: 12px" v-model="selectedWords.criminal">
              <el-checkbox class="tagContent" v-for="word in item" :label="word" :key="word">
                {{word}}
              </el-checkbox>
            </el-checkbox-group>
         <div style="background:linear-gradient(to left,#F0F0F0,#b6b6b6,#F0F0F0);
    height:1px;
    position: relative;
    margin-bottom: 9px"></div>
       </div>
       <div>
         <span style="font-family: 方正苏新诗柳楷简体;
    font-size: larger;
    font-weight: bold;
    margin-top: 10px;
    margin-right: 40px">补充标记:</span>
         <el-input
             style="margin-top: 10px;
             width: 55%;"
             placeholder="如果您觉得系统分词不准确，可在此手动添加标记"
             v-model="complement_mark.criminal"
             clearable
             >
         </el-input>
       </div>
     </el-tab-pane>
     <el-tab-pane label="性别">
       <div style="text-align: left" v-for="(item, word, index) of tag" :key="index">
         <!--            span里是词性标题-->
         <span class="tagTitle" v-if="word === 'noun'">名词</span>
         <span class="tagTitle" v-if="word === 'verb'">动词</span>
         <span class="tagTitle" v-if="word === 'adjectives'">形容词</span>
         <span class="tagTitle" v-if="word === 'adverb'">副词</span>
         <!--            下面是复选框-->
         <el-checkbox-group style="margin-bottom: 10px" v-model="selectedWords.sex">
           <el-checkbox class="tagContent" v-for="word in item" :label="word" :key="word">
             {{word}}
           </el-checkbox>
         </el-checkbox-group>
         <div style="background:linear-gradient(to left,#F0F0F0,#b6b6b6,#F0F0F0);
    height:1px;
    position: relative;
    margin-bottom: 10px"></div>
       </div>
       <div>
         <span style="font-family: 方正苏新诗柳楷简体;
    font-size: larger;
    font-weight: bold;
    margin-top: 10px;
    margin-right: 40px">补充标记:</span>
         <el-input
             style="margin-top: 10px;
             width: 55%;"
             placeholder="如果您觉得系统分词不准确，可在此手动添加标记"
             v-model="complement_mark.sex"
             clearable
         >
         </el-input>
       </div>
     </el-tab-pane>
     <el-tab-pane label="民族">
       <div style="text-align: left" v-for="(item, word, index) of tag" :key="index">
         <!--            span里是词性标题-->
         <span class="tagTitle" v-if="word === 'noun'">名词</span>
         <span class="tagTitle" v-if="word === 'verb'">动词</span>
         <span class="tagTitle" v-if="word === 'adjectives'">形容词</span>
         <span class="tagTitle" v-if="word === 'adverb'">副词</span>
         <!--            下面是复选框-->
         <el-checkbox-group style="margin-bottom: 10px" v-model="selectedWords.ethic">
           <el-checkbox class="tagContent" v-for="word in item" :label="word" :key="word">
             {{word}}
           </el-checkbox>
         </el-checkbox-group>
         <div style="background:linear-gradient(to left,#F0F0F0,#b6b6b6,#F0F0F0);
    height:1px;
    position: relative;
    margin-bottom: 10px"></div>
       </div>
       <div>
         <span style="font-family: 方正苏新诗柳楷简体;
    font-size: larger;
    font-weight: bold;
    margin-top: 10px;
    margin-right: 40px">补充标记:</span>
         <el-input
             style="margin-top: 10px;
             width: 55%;"
             placeholder="如果您觉得系统分词不准确，可在此手动添加标记"
             v-model="complement_mark.ethic"
             clearable
         >
         </el-input>
       </div>
     </el-tab-pane>
     <el-tab-pane label="出生地">
       <div style="text-align: left" v-for="(item, word, index) of tag" :key="index">
         <!--            span里是词性标题-->
         <span class="tagTitle" v-if="word === 'noun'">名词</span>
         <span class="tagTitle" v-if="word === 'verb'">动词</span>
         <span class="tagTitle" v-if="word === 'adjectives'">形容词</span>
         <span class="tagTitle" v-if="word === 'adverb'">副词</span>
         <!--            下面是复选框-->
         <el-checkbox-group style="margin-bottom: 10px" v-model="selectedWords.birth">
           <el-checkbox class="tagContent" v-for="word in item" :label="word" :key="word">
             {{word}}
           </el-checkbox>
         </el-checkbox-group>
         <div style="background:linear-gradient(to left,#F0F0F0,#b6b6b6,#F0F0F0);
    height:1px;
    position: relative;
    margin-bottom: 10px"></div>
       </div>
       <div>
         <span style="font-family: 方正苏新诗柳楷简体;
    font-size: larger;
    font-weight: bold;
    margin-top: 10px;
    margin-right: 40px">补充标记:</span>
         <el-input
             style="margin-top: 10px;
             width: 55%;"
             placeholder="如果您觉得系统分词不准确，可在此手动添加标记"
             v-model="complement_mark.birth"
             clearable
         >
         </el-input>
       </div>
     </el-tab-pane>
     <el-tab-pane label="案由">
       <div style="text-align: left" v-for="(item, word, index) of tag" :key="index">
         <!--            span里是词性标题-->
         <span class="tagTitle" v-if="word === 'noun'">名词</span>
         <span class="tagTitle" v-if="word === 'verb'">动词</span>
         <span class="tagTitle" v-if="word === 'adjectives'">形容词</span>
         <span class="tagTitle" v-if="word === 'adverb'">副词</span>
         <!--            下面是复选框-->
         <el-checkbox-group style="margin-bottom: 10px" v-model="selectedWords.reason">
           <el-checkbox class="tagContent" v-for="word in item" :label="word" :key="word">
             {{word}}
           </el-checkbox>
         </el-checkbox-group>
         <div style="background:linear-gradient(to left,#F0F0F0,#b6b6b6,#F0F0F0);
    height:1px;
    position: relative;
    margin-bottom: 10px"></div>
       </div>
       <div>
         <span style="font-family: 方正苏新诗柳楷简体;
    font-size: larger;
    font-weight: bold;
    margin-top: 10px;
    margin-right: 40px">补充标记:</span>
         <el-input
             style="margin-top: 10px;
             width: 55%;"
             placeholder="如果您觉得系统分词不准确，可在此手动添加标记"
             v-model="complement_mark.reason"
             clearable
         >
         </el-input>
       </div>
     </el-tab-pane>
     <el-tab-pane label="相关法院">

       <div style="text-align: left" v-for="(item, word, index) of tag" :key="index">
         <!--            span里是词性标题-->
         <span class="tagTitle" v-if="word === 'noun'">名词</span>
         <span class="tagTitle" v-if="word === 'verb'">动词</span>
         <span class="tagTitle" v-if="word === 'adjectives'">形容词</span>
         <span class="tagTitle" v-if="word === 'adverb'">副词</span>
         <!--            下面是复选框-->
         <el-checkbox-group style="margin-bottom: 10px" v-model="selectedWords.lawHall">
           <el-checkbox class="tagContent" v-for="word in item" :label="word" :key="word">
             {{word}}
           </el-checkbox>
         </el-checkbox-group>

         <div style="background:linear-gradient(to left,#F0F0F0,#b6b6b6,#F0F0F0);
    height:1px;
    position: relative;
    margin-bottom: 10px"></div>
       </div>
       <div>
         <span style="font-family: 方正苏新诗柳楷简体;
    font-size: larger;
    font-weight: bold;
    margin-top: 10px;
    margin-right: 40px">补充标记:</span>
         <el-input
             style="margin-top: 10px;
             width: 55%;"
             placeholder="如果您觉得系统分词不准确，可在此手动添加标记"
             v-model="complement_mark.lawHall"
             clearable
         >
         </el-input>
       </div>
     </el-tab-pane>
   </el-tabs>

   <el-button style="margin-top: 30px" size="small" type="primary" @click="saveAndSendMark()">保存案件与标注</el-button>

   <fieldset class="text-intro3">
     <legend>自动化深度分词</legend>
     <legend>后端算法基于语义和反馈学习的分词</legend>
   </fieldset>

<!--   新加的语义分词结果-->
   <el-tabs class="tag" type="border-card">
     <el-tab-pane label="数据可视化">
       <div v-if="isShow"><img :src="url_criminal" style="width: 60%"></div>
       <div class="tagTitle" style="margin-top: 20px; margin-bottom: 20px" v-if="isShow">罪犯相关信息</div>
       <el-divider v-if="isShow"></el-divider>
       <div v-if="isShow"><img :src="url_case" style="width: 60%"></div>
       <div class="tagTitle" style="margin-top: 20px; margin-bottom: 20px" v-if="isShow">案件相关信息</div>
       <el-divider v-if="isShow"></el-divider>
       <div v-if="isShow"><img :src="url_hall" style="width: 60%"></div>
       <div class="tagTitle" style="margin-top: 20px; margin-bottom: 20px" v-if="isShow">法院相关信息</div>
       <el-divider v-if="isShow"></el-divider>
     </el-tab-pane>
     <el-tab-pane label="当事人">
<!--        <ul>-->
          <span style="text-align: right;display:inline-block" v-for="word in preciserWords.criminal" :key="word">
            <span >🔷</span>
            {{word}}
            <el-divider></el-divider>
          </span>

<!--        </ul>-->
     </el-tab-pane>
     <el-tab-pane label="性别">
       <span style="text-align: right;display:inline-block" v-for="word in preciserWords.sex" :key="word">
         <span >🔷</span>
            {{word}}   &ensp;
         <el-divider></el-divider>
       </span>
     </el-tab-pane>
     <el-tab-pane label="民族">
       <span style="text-align: right;display:inline-block" v-for="word in preciserWords.ethic" :key="word">
            <span >🔷</span>
            {{word}}   &ensp;
         <el-divider></el-divider>
       </span>
     </el-tab-pane>
     <el-tab-pane label="户籍地">
       <span style="text-align: right;display:inline-block" v-for="word in preciserWords.birthPlace" :key="word">
            <span >🔷</span>
            {{word}}   &ensp;
         <el-divider></el-divider>
       </span>
     </el-tab-pane>
     <el-tab-pane label="案由">
       <span style="text-align: right;display:inline-block" v-for="word in preciserWords.reason" :key="word">
            <span >🔷</span>
            {{word}}   &ensp;
         <el-divider></el-divider>
       </span>
     </el-tab-pane>
     <el-tab-pane label="相关地点">
       <span style="text-align: right;display:inline-block" v-for="word in preciserWords.spot" :key="word">
            <span >🔷</span>
            {{word}}   &ensp;
         <el-divider></el-divider>
       </span>
     </el-tab-pane>
     <el-tab-pane label="相关时间">
       <span style="text-align: right;display:inline-block" v-for="word in preciserWords.time" :key="word">
            <span >🔷</span>
            {{word}}   &ensp;
         <el-divider></el-divider>
       </span>
     </el-tab-pane>
     <el-tab-pane label="出生时间">
       <span style="text-align: right;display:inline-block" v-for="word in preciserWords.birthTime" :key="word">
            <span >🔷</span>
            {{word}}   &ensp;
         <el-divider></el-divider>
       </span>
     </el-tab-pane>
     <el-tab-pane label="相关法院">
       <span style="text-align: right;display:inline-block;" v-for="word in preciserWords.lawHall" :key="word">
            <span >🔷</span>
            {{word}}   &ensp;
         <el-divider></el-divider>
       </span>
<!--       <div><img src="../assets/criminal.jpg" style="width: 60%"></div>-->
     </el-tab-pane>
   </el-tabs>


   <P id="tip">
     文本信息来源：裁判文书网
   </P>
   <el-button  type="success" icon="el-icon-check" circle @click="paintedEggShell"></el-button>
   <br>

 </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'example',
  data(){
    return{
      test:'BAD TRAP',
      timeValue: '',
      textValue: '',
      //category代表分词的词性
      //words是分词结果
      tag:{
        // noun:['test10','test12','test13','test14','test15','test16','test17'],
        // verb:['test20','test21','test22','test23','test24','test25','test26','test27'],
        // adjectives:['test30','test31','test32','test33','test34','test35','test36','test37'],
        // adverb:['test40','test41','test42','test43','test44','test45','test46','test47']
        noun:[],
        verb:[],
        adjectives:[],
        adverb:[]
      },
      //selectedWords存储分词的结果
      selectedWords: {
        criminal:[],
        sex:[],
        ethic:[],
        birth:[],
        reason:[],
        lawHall:[]
      },
      //后端传过来的语义分词结果
      preciserWords:{
        criminal:[],
        sex:[],
        ethic:[],
        birthPlace:[],
        reason:[],
        spot:[],
        time:[],
        birthTime:[],
        lawHall:[]
      },
      isShow: false,
      url_criminal: '',
      url_case: '',
      url_hall: '',
      //补充分词结果
      complement_mark:{
        criminal:'',
        sex:'',
        ethic:'',
        birth:'',
        reason:'',
        lawHall:''
      }
    }
  },
  methods: {
    onSpider: function (){
      if(this.timeValue.length === 0){
        this.$alert('请选择案件时间进行自动化爬取！', '未选择时间', {
          confirmButtonText: '确定',
        });
      }
      else{
        //前后端通信
        const path = 'http://localhost:5000/onSpider';
        var timeData = {
          startTime : this.timeValue[0].toLocaleDateString(),
          endTime : this.timeValue[1].toLocaleDateString()
        }
        console.log(timeData.startTime, timeData.endTime)
        //弹窗提示
        this.$alert('正在自动爬取案件...爬取文件保存于本地', '请稍候', {
          confirmButtonText: '确定',
        });
        axios({
          method : "post",
          url : path,
          data: timeData
        }).then((res) => {
              console.log(res.data)
              //弹窗提示
              this.$alert('已成功按标注日期自动爬取案件！爬取文件保存于本地', '爬取成功', {
                confirmButtonText: '确定',
              });
            })
      }
    },
    openFile: function(file) {
      var reader = new FileReader();
      var that = this
      reader.onload = function () {
        if (reader.result) {
          //打印文件内容
          that.textValue = reader.result
          console.log(that.textValue)
        }
      };
      reader.readAsText(file.raw);
    },
    nlpText: function (){
      const path = '/api/onNLP';
      const that = this;
      var text = {
        text : this.textValue
      }
      axios({
        method : "post",
        url : path,
        data: text
      }).then((res) => {
        that.preciserWords.criminal = res.data.criminal;
        that.preciserWords.sex = res.data.sex;
        that.preciserWords.ethic = res.data.ethic;
        that.preciserWords.birthPlace = res.data.birthPlace;
        that.preciserWords.reason = res.data.reason;
        that.preciserWords.spot = res.data.spot;
        that.preciserWords.time = res.data.time;
        that.preciserWords.birthTime = res.data.birthTime;
        that.preciserWords.lawHall = res.data.lawHall;
        console.log('NLP ok.')
        //数据可视化
        //回调时把词云显示到前端
        that.isShow = true;
        that.url_criminal = require('../assets/criminal.jpg')
        that.url_case = require('../assets/case.jpg')
        that.url_hall = require('../assets/hall.jpg')
      })
    },
    splitText: function (){
      //如果未输入案例文本或者未选择文件
      if(this.textValue.length === 0){
        this.$alert('请键入或选择爬取的案件txt文件！', '案件信息为空', {
          confirmButtonText: '确定',
        });
      }
      else{
        //调用hanlp，进行自动分词
        this.nlpText();
        //把后端数据返回前端
        const path = '/api/onSplit';
        const that = this;
        var text = {
          text : this.textValue
        }
        axios({
          method : "post",
          url : path,
          data: text
        }).then((res) => {
          //后端返回字典，传入前端数据
          that.tag.noun = res.data.noun;
          that.tag.verb = res.data.verb;
          that.tag.adjectives = res.data.adjectives;
          that.tag.adverb = res.data.adverb;
          console.log('split ok')
          // console.log(that.tag.noun)
          // console.log(that.tag.verb)
          // console.log(that.tag.adjectives)
          // console.log(that.tag.adverb)
        })
        // axios({
        //   method : "post",
        //   url : 'http://localhost:5000/onNLP2',
        //   data: text
        // }).then((res) => {
        //   //后端返回字典，传入前端数据
        //   that.preciserWords.criminal = res.data.criminal;
        //   that.preciserWords.sex = res.data.sex;
        //   that.preciserWords.ethic = res.data.ethic;
        //   that.preciserWords.birthPlace = res.data.birthPlace;
        //   that.preciserWords.reason = res.data.reason;
        //   that.preciserWords.spot = res.data.spot;
        //   that.preciserWords.time = res.data.time;
        //   that.preciserWords.birthTime = res.data.birthTime;
        //   that.preciserWords.lawHall = res.data.lawHall;
        //   console.log('NLP2 ok')
        // })
        //Alert
        this.$alert('已成功进行分词！', '案例分词', {
          confirmButtonText: '确定',
        });
      }
    },
    saveAndSendMark: function (){
      //如果没有选择标注
      const criminalLen = this.selectedWords.criminal.length;
      const sexLen = this.selectedWords.sex.length;
      const reasonLen = this.selectedWords.reason.length;
      const ethicLen = this.selectedWords.ethic.length;
      const lawHallLen = this.selectedWords.lawHall.length;
      const birthLen = this.selectedWords.birth.length;
      const comple_criminalLen = this.complement_mark.criminal.length;
      const comple_sexLen = this.complement_mark.sex.length;
      const comple_reasonLen = this.complement_mark.reason.length;
      const comple_ethicLen = this.complement_mark.ethic.length;
      const comple_lawHallLen = this.complement_mark.lawHall.length;
      const comple_birthLen = this.complement_mark.birth.length;
      if(criminalLen === 0 && sexLen === 0 && reasonLen === 0 && ethicLen === 0 && lawHallLen === 0 && birthLen === 0){
        this.$alert('请按照您的需求进行标注！', '标注为空', {
          confirmButtonText: '确定',
        });
      }
      else {
        console.log('ok')
        if(comple_criminalLen !== 0){
          this.selectedWords.criminal.push(this.complement_mark.criminal)
        }
        if(comple_sexLen !== 0){
          this.selectedWords.sex.push(this.complement_mark.sex)
        }
        if(comple_reasonLen !== 0){
          this.selectedWords.reason.push(this.complement_mark.reason)
        }
        if(comple_ethicLen !== 0){
          this.selectedWords.ethic.push(this.complement_mark.ethic)
        }
        if(comple_lawHallLen !== 0){
          this.selectedWords.lawHall.push(this.complement_mark.lawHall)
        }
        if(comple_birthLen !== 0){
          this.selectedWords.birth.push(this.complement_mark.birth)
        }
        var markResult
        const path = 'http://localhost:5000/onMark';
        const that = this;
        markResult = {
          criminal: that.selectedWords.criminal,
          sex: that.selectedWords.sex,
          ethic: that.selectedWords.ethic,
          birth: that.selectedWords.birth,
          reason: that.selectedWords.reason,
          lawHall: that.selectedWords.lawHall
        }
        axios({
          method : "post",
          url : path,
          data: markResult
        }).then((res) => {
          console.log(res.data)
        })
        this.$alert('标注结果已保存至本地！', '标注成功', {
          confirmButtonText: '确定',
        });
        console.log(this.selectedWords)
      }
    },
    //彩蛋
    paintedEggShell: function (){
      // const path = 'http://localhost:5000/data-science';
      // axios.get(path)
      //     .then((res) => {
      //       this.test = res.data;
      //     })
      //     .catch((error) => {
      //       // eslint-disable-next-line
      //       console.error(error);
      //     });
      this.$alert('开发者及分工：郑周斌-分词标注|刘心怡-爬虫|彭俊植-前后端 南京大学软件学院✨', '感谢使用', {
        confirmButtonText: '确定',
      });
    }
  }
}
</script>

<style scoped>

  .spider-intro{
    margin-top: 20px;
    border: 0;
    font-size: large;
    font-family: 方正苏新诗柳楷简体;
    font-weight: bold;
  }

  .block{
    margin-top: 0;
    position: relative;
    height: 60px;
    width: 44%;
    margin-left: 28%;
    /*border-radius: 30px;*/
    /*border:1px solid #2c3e50*/
  }

  .text-intro {
    margin-top: 20px;
    border: 0;
    border-top: 2px solid #ddd;
    text-align: center;
  }
  legend {
    font-family: 方正苏新诗柳楷简体;
    font-size: large;
    font-weight: bold;
    padding: 0 5%;
  }
  .button-group{
    position: relative;
  }

  #spider{
    margin-left: 20px;
  }

  .splitword-button{
    margin-top: 20px;
    margin-left: 12px;
    position: absolute;
  }

  .test{
    align-content: center;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    height : 240px;
    width: 50%;
    margin-left: 25%;
  }

  .upload-demo{
    margin-left: 40%;
    margin-top: 20px;
    position: absolute;
  }

  #caseText{
    width: 60%;
    margin-left: 14%;
    margin-top: 20px;

  }

  .text-intro2 {
    margin-top: 110px;
    border: 0;
    border-top: 2px solid #ddd;
    text-align: center;
  }

  .text-intro3 {
    margin-top: 40px;
    border: 0;
    border-top: 2px solid #ddd;
    text-align: center;
  }

  .tag{
    margin-top: 20px;
    width: 50%;
    margin-left: 25%;
  }

  .tagTitle{
    font-family: "思源宋体 CN Heavy";
    font-size: large;
    font-weight: normal;
  }

  .tagContent{
    font-family: "Adobe Caslon Pro Bold";
    font-size: large;
    margin-top: 10px;
  }

  #tip{
    margin-top: 30px;
    font-family: 方正苏新诗柳楷简体;
    font-weight: bold;
    font-size: large;
  }
</style>
