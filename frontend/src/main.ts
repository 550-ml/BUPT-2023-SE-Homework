import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
// import router from "./router/router.ts";
import { createRouter, createWebHistory } from "vue-router";

import HomeView from "./views/HomeView.vue";
import Login from "./views/login/index.vue";
import Register from "./views/login/register.vue";
import Administrator from "./views/Administrator/Administrator.vue";

import Panel1 from "./router/AirConditionerManage.vue";
import Panel2 from "./router/BillGenerate.vue";
import Panel3 from "./router/HotelManage.vue";

const routes = [
    {
        path: "/",
        name: "home",
        component: HomeView,
        children: [
            { path: "panel1", component: Panel1 },
            { path: "panel2", component: Panel2 },
            { path: "panel3", component: Panel3 }
        ]
    },
    {
        path: "/login",
        name: "login",
        component: Login
    },
    {
        path: "/register",
        name: "register",
        component: Register
    },
    {
        path: "/administrator",
        name: "administrator",
        component: Administrator
    }
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
});

const app = createApp(App);
// 导入style 文件
import "./styles/index.scss";

app.use(router).mount("#app");
