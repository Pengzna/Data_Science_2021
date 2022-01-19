// import Vue from "vue"
// import Router from "vue-router"
import charts from "@/components/charts";
// import {createRouter, createWebHistory} from 'vue-router'

import { createRouter } from 'vue-router'

const routes = [
    {
        path : '/charts',
        component: charts
    }
]

const router = createRouter({
    routes
})


// Vue.use(Router)
//
// const router = new Router({
//     routes: [
//         { path: '/charts', component : charts},
//         { path: '/', component: analyse}
//     ]
// })
//
export default router
