/**
 * 该文件是整个项目的入口文件
 */
//引入Vue组件
// import Vue from 'vue'
// 引入App组件，它是所有组件的父组件
// import App from './App.vue'

import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';
// import router from './router'

Vue.use(ElementUI);
// 关闭vue的生产提示
Vue.config.productionTip = false


// // 5. 创建并挂载根实例
// const app = Vue.createApp({})
// app.use(router)
// app.mount('#app')

//$mount相当于el
new Vue({
  //h是render的参数，h是一个函数，叫createElement
  render: h => h(App),
  // router
}).$mount('#app')
// console.log(64136)
