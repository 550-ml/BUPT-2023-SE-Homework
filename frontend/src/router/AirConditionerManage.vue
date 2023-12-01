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
                  <img src="../assets/room1.jpg" class="image" />
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
import { ref } from "vue";
// declare function require(img: string): string;  // 声明
const roomsInfo = ref([
  {
    roomId: 'Room 1',
    mode: 'Cold',
    speed: 'Medium',
    currTemp: '20°C',
    targetTemp: '25°C',
    servedTime: '2 hours',
    fee: '$15',
    // image: require('../assets/room1.jpg')
  },
  {
    roomId: 'Room 2',
    mode: 'Hot',
    speed: 'High',
    currTemp: '30°C',
    targetTemp: '28°C',
    servedTime: '3 hours',
    fee: '$20',
    // image: require('../assets/room2.jpg')
  },
  {
    roomId: 'Room 2',
    mode: 'Hot',
    speed: 'High',
    currTemp: '30°C',
    targetTemp: '28°C',
    servedTime: '3 hours',
    fee: '$20',
    image: '../assets/room3.jpg'
  }, {
    roomId: 'Room 1',
    mode: 'Cold',
    speed: 'Medium',
    currTemp: '20°C',
    targetTemp: '25°C',
    servedTime: '2 hours',
    fee: '$15',
    image: '../assets/room4.jpg'
  },
  {
    roomId: 'Room 1',
    mode: 'Cold',
    speed: 'Medium',
    currTemp: '20°C',
    targetTemp: '25°C',
    servedTime: '2 hours',
    fee: '$15',
    image: '../assets/room5.jpg'
  }
  // Add more rooms as needed...
])

// This code keeps track of the current date and time
const currentDate = ref(new Date());
setInterval(() => {
  currentDate.value = new Date();
}, 1000);
</script>

<style lang="scss">
/* 全局样式 */
.common-layout {
  height: 100vh;
  padding: 0;
  /* 设置整个布局高度为视窗的高度 */
}

/* 定义el-header元素的样式 */
.el-header {
  background-color: #111619;
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

/* 左边那一栏文字 */
.el-tabs--left .el-tabs__item.is-left {
  font-size: 25px;
  color: #333;
  font-family: Arial, sans-serif;
  font-weight: bold;
  line-height: 1.5;
  text-decoration: none;
  text-transform: uppercase;
}

.el-tab-pane {
  padding: 50px;
}

/* 主要内容样式 */
.show-mes {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin: 0;
  /* 去除外边距 */
  padding: 0;
  /* 去除内边距 */
  justify-content: space-evenly;
}

.el-card {
  width: calc(33.33% - 20px);
  margin-bottom: 20px;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 添加阴影效果 */
  background-color: rgb(216, 210, 210);
  /* 设置背景色 */
  transition: box-shadow 0.3s ease;
  /* 添加阴影过渡效果 */
}

.el-card:hover {
  box-shadow: 0 50px 50px rgba(13, 88, 180, 0.15);
  /* 改变阴影效果 */
}

/* 设置图片样式 */
.image {
  width: 95%;
  max-width: 100%;
  display: block;
  margin: 0 auto;
  margin-bottom: 10px;
  border-radius: 20px 20px 10px 10px;
  /* 图片上方设置圆角 */
}

.show-mes .bottom {
  line-height: 1.5;
  font-size: 18px;
}

/* 按钮样式 */
.button {
  padding: 8px 16px;
  border-radius: 5px;
  background-color: #007BFF;
  color: #a01818;
  transition: background-color 0.3s ease;
  /* 添加背景色过渡效果 */
}

.button:hover {
  background-color: #0056b3;
  /* 鼠标悬停时改变背景色 */
}

.time {
  font-size: 12px;
  color: #999;
}
</style>

