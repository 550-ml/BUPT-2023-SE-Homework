<template>
    <div class="common-layout">
        <el-container>
            <el-header height="200px">
                <div class="head-text">空调管理员界面</div>
            </el-header>
            <el-container>
                <!-- <el-aside width="200px">
                    <el-tabs type="border-card" tab-position="left">
                        <el-tab-pane label="空调运行">空调运行</el-tab-pane>
                        <el-tab-pane label="设置空调">设置空调</el-tab-pane>
                    </el-tabs>
                </el-aside> -->
                <el-main>
                    <el-tabs type="border-card" tab-position="left">
                        <el-tab-pane label="空调运行" class="left-text">
                            <div class="show-mes">
                                <el-card v-for="(room, index) in roomsInfo" :key="index">
                                    <img src="../../assets/room1.jpg" class="image" />
                                    <div style="padding: 14px">
                                        <span>{{ room.roomId }}</span>
                                        <div class="bottom">
                                            <p>空调模式: {{ room.mode }}</p>
                                            <p>当前风速: {{ room.speed }}</p>
                                            <p>当前温度: {{ room.currTemp }}</p>
                                            <p>目标温度: {{ room.targetTemp }}</p>
                                            <p>服务时间: {{ room.servedTime }}</p>
                                            <p>服务费用: {{ room.fee }}</p>
                                            <el-button text class="button">操作</el-button>
                                        </div>
                                    </div>
                                </el-card>
                            </div>
                        </el-tab-pane>
                        <el-tab-pane label="设置空调" class="left-text">设置空调</el-tab-pane>
                    </el-tabs>
                </el-main>
            </el-container>
            <el-footer>Footer</el-footer>
        </el-container>
    </div>
</template>


<script lang="ts" setup>
import { ref } from 'vue'

const roomsInfo = ref([
    {
        roomId: 'Room 1',
        mode: 'Cold',
        speed: 'Medium',
        currTemp: '20°C',
        targetTemp: '25°C',
        servedTime: '2 hours',
        fee: '$15'
    },
    {
        roomId: 'Room 2',
        mode: 'Hot',
        speed: 'High',
        currTemp: '30°C',
        targetTemp: '28°C',
        servedTime: '3 hours',
        fee: '$20'
    },
    {
        roomId: 'Room 2',
        mode: 'Hot',
        speed: 'High',
        currTemp: '30°C',
        targetTemp: '28°C',
        servedTime: '3 hours',
        fee: '$20'
    }, {
        roomId: 'Room 1',
        mode: 'Cold',
        speed: 'Medium',
        currTemp: '20°C',
        targetTemp: '25°C',
        servedTime: '2 hours',
        fee: '$15'
    },
    {
        roomId: 'Room 1',
        mode: 'Cold',
        speed: 'Medium',
        currTemp: '20°C',
        targetTemp: '25°C',
        servedTime: '2 hours',
        fee: '$15'
    }
    // Add more rooms as needed...
])

// This code keeps track of the current date and time
const currentDate = ref(new Date())
setInterval(() => {
    currentDate.value = new Date()
}, 1000)
</script>

<style>
/* 全局样式 */
.common-layout {
    height: 100vh;
    /* 设置整个布局高度为视窗的高度 */
}

/* 定义el-header元素的样式 */
.el-header {
    background-color: #3498db;
    /* 背景颜色 */
    color: #ffffff;
    /* 文本颜色 */
    padding: 20px;
    /* 内边距 */
    text-align: center;
    /* 文本居中 */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    /* 阴影效果 */
}

/* 定义head-text类的样式 */
.head-text {
    font-size: 80px;
    /* 字体大小 */
    font-weight: bold;
    /* 字体加粗 */
}


.el-tabs {
    flex: 1;
    height: 100%;
    /* 使用 el-aside 的高度 */

}

.el-tab-pane {
    padding: 200px;
}

.el-tabs__content {
    padding: 200px;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
}

.left-text {
    font-size: 24px;
}

/* 主要内容样式 */
.show-mes {
    display: flex;
    flex-wrap: wrap;
    /* 使用 flex 布局，让 el-card 水平排列，并换行显示 */
    gap: 20px;
    /* 设置元素之间的间距 */
}

.el-card {
    width: calc(33.33% - 20px);
    /* 设置每个 el-card 的宽度为三分之一，减去间距 */
    margin-bottom: 20px;
    /* 设置下边距 */
}

.image {
    width: 100%;
    max-width: 100%;
    display: block;
    margin-bottom: 10px;
    /* 调整图片样式 */
}

.show-mes .bottom {
    line-height: 1.5;
    font-size: 16px;
    /* 调整文字样式 */
}

.button {
    padding: 0;
    min-height: auto;
}

.time {
    font-size: 12px;
    color: #999;
}
</style>

