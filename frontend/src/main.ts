import {createApp} from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
// 导入element-plus整体
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
const app = createApp(App)
app.use(ElementPlus)
app.mount('#app')
// 导入style 文件
import './styles/index.scss'

createApp(App).use(router).mount('#app')