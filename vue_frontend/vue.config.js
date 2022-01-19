// module.exports = {
//     devServer: {
//         port: 9090,
//         //配置跨域访问
//         proxy: {
//             '/data-science': {
//                 target: 'http://localhost:5000',
//                 changeOrigin: true,
//                 ws : true,
//                 // pathRewrite: {
//                 //     '^/api': 'http://localhost:5000/data-science'  //路径重写
//                 // }
//             },
//         }
//     }
// }
//跨域配置
module.exports = {
    devServer: {                //记住，别写错了devServer//设置本地默认端口  选填
        // port: 9876,
        proxy: {                 //设置代理，必须填
            '/api': {              //设置拦截器  拦截器格式   斜杠+拦截器名字，名字可以自己定
                target: 'http://localhost:5000',     //代理的目标地址
                changeOrigin: true,              //是否设置同源，输入是的
                pathRewrite: {                   //路径重写
                    '/api': ''                     //选择忽略拦截器里面的单词
                }
            }
        }
    }
}
