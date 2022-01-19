# 2021秋 数据科学基础大作业 司法大数据自动化标注与分析

## 项目技术栈

- **前端**：Vue，Axios，ElementUI

- **后端**：flask

  - **NLP** ：hanlp、TF-IDF、textrank、朴素贝叶斯、机器学习

  - **爬虫**：Selenium

## 代码结构

```bash
|-- data-science # 前后端分离项目
    |-- .idea
    |-- flask_backend # 后端文件
    |   |-- app.py # 后端主入口
    |   |-- .idea
    |   |-- case_txt
    |   |-- crawler # 爬虫
    |   |-- json_result # 前端标注结果
    |   |-- mark # NLP
    |   |-- test_case
    |   |-- util
    |   |-- word_cloud # 数据可视化
    | 
    |-- vue_frontend # 前端文件    
        |-- babel.config.js
        |-- package-lock.json
        |-- package.json
        |-- vue.config.js
        |-- .idea
        |-- public
        |-- src
            |-- App.vue
            |-- main.js
            |-- assets # 静态资源
            |-- components # 前端组件
            |-- router # 路由
```

## 项目启动

后端：

- 进入`flask_backend`文件夹，点击右上角修改编译配置，确保项目`working directory`位于目录`flask_backend`
  - [![7ss8oj.png](https://s4.ax1x.com/2022/01/19/7ss8oj.png)](https://imgtu.com/i/7ss8oj)
  - [![7ss1eg.png](https://s4.ax1x.com/2022/01/19/7ss1eg.png)](https://imgtu.com/i/7ss1eg)
- 使用`pip install xxx`命令安装缺失的依赖（可根据pycharm IDE提示安装）
- 进入`flask_backend`文件夹，运行`app.py`文件，可见后台运行于`http://127.0.0.1:5000/`

前端：

- 进入`vue_frontend`文件夹，执行命令：

```
npm install
```

```
npm run serve
```
即可于`http://localhost:8080/ `启动前台vue工程

## 如何使用

- 访问`http://localhost:8080/` 进入项目

[![7ssJFs.png](https://s4.ax1x.com/2022/01/19/7ssJFs.png)](https://imgtu.com/i/7ssJFs)

- 选定具体时间区间，自动化爬取选定时间区间的案例文书

[![7ssQOS.png](https://s4.ax1x.com/2022/01/19/7ssQOS.png)](https://imgtu.com/i/7ssQOS)

- 在文本框手动输入案例或者上传本地案例文件，点击“开始分词”进行自动化分词

[![7ss3wQ.png](https://s4.ax1x.com/2022/01/19/7ss3wQ.png)](https://imgtu.com/i/7ss3wQ)

[![7sstWq.png](https://s4.ax1x.com/2022/01/19/7sstWq.png)](https://imgtu.com/i/7sstWq)

- 随后可以在页面看到后端的分词结果，用户可以进行手动标注。点击下方按钮保存标注结果。标注结果将以json格式保存到本地。

[![7ssUS0.png](https://s4.ax1x.com/2022/01/19/7ssUS0.png)](https://imgtu.com/i/7ssUS0)

[![7ssalV.png](https://s4.ax1x.com/2022/01/19/7ssalV.png)](https://imgtu.com/i/7ssalV)

[![7ssyk9.png](https://s4.ax1x.com/2022/01/19/7ssyk9.png)](https://imgtu.com/i/7ssyk9)

- 同时，前端会显示后端基于hanlp和反馈学习的自动化标注结果，并展示词云可视化结果，供用户参考

[![7ssdyT.png](https://s4.ax1x.com/2022/01/19/7ssdyT.png)](https://imgtu.com/i/7ssdyT)

[![7ssDw4.png](https://s4.ax1x.com/2022/01/19/7ssDw4.png)](https://imgtu.com/i/7ssDw4)

[![7ssBmF.png](https://s4.ax1x.com/2022/01/19/7ssBmF.png)](https://imgtu.com/i/7ssBmF)

[![7ssrTJ.png](https://s4.ax1x.com/2022/01/19/7ssrTJ.png)](https://imgtu.com/i/7ssrTJ)

## 开发者

- 郑周斌：NLP
- 刘心怡：爬虫
- 彭俊植：前后端、可视化

©南京大学软件学院
