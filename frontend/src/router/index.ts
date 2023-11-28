import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";
import Login from "../views/login/index.vue";
import Register from "../views/login/register.vue";
import Administrator from "../views/Administrator/Administrator.vue";
const routes = [
    {
        path: "/",
        name: "home",
        component: HomeView
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

export default router;
