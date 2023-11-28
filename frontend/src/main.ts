import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import router from "./router/router.ts";

const app = createApp(App);
// 导入style 文件
import "./styles/index.scss";

app.use(router).mount("#app");
