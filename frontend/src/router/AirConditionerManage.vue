<template>
  <div class="common-layout">
    <el-container>
      <el-header height="200px">
        <div class="head-text">空调管理员界面</div>
      </el-header>
      <el-container>
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
            <el-tab-pane label="设置参数" class="left-text">
              <el-form label-width="200px" size="large" class="custom-form">
                <el-form-item label="默认模式">
                  <el-radio-group>
                    <el-radio label="hot">hot</el-radio>
                    <el-radio label="cold">cold</el-radio>
                  </el-radio-group>
                </el-form-item>

                <el-form-item label="制冷温控区间">
                  <el-row>
                    <el-col :span="8" :offset="2">
                      <el-input type="number" placeholder="最低温度"></el-input>
                    </el-col>
                    <el-col :span="1" :offset="1">-</el-col>
                    <el-col :span="8" :offset="1">
                      <el-input type="number" placeholder="最高温度"></el-input>
                    </el-col>
                  </el-row>
                </el-form-item>

                <el-form-item label="制热温控区间">
                  <el-row>
                    <el-col :span="8" :offset="2">
                      <el-input type="number" placeholder="最低温度"></el-input>
                    </el-col>
                    <el-col :span="1" :offset="1">-</el-col>
                    <el-col :span="8" :offset="1">
                      <el-input type="number" placeholder="最高温度"></el-input>
                    </el-col>
                  </el-row>
                </el-form-item>

                <el-form-item label="缺省温度">
                  <el-row>
                    <el-col :span="8" :offset="8">
                      <el-input type="number" placeholder="缺省温度"></el-input>
                    </el-col>
                  </el-row>
                </el-form-item>

                <el-form-item label="费率">
                  <el-row>
                    <el-col :span="8" :offset="8">
                      <el-input type="number" placeholder="费率"></el-input>
                    </el-col>
                  </el-row>
                </el-form-item>

                <el-form-item label="服务对象数">
                  <el-row>
                    <el-col :span="8" :offset="8">
                      <el-input type="number" placeholder="服务对象数"></el-input>
                    </el-col>
                  </el-row>
                </el-form-item>

                <el-form-item>
                  <el-button type="primary" class="custom-button">
                    设置默认参数
                  </el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
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

.custom-form {
  padding: 30px;
  /* 增加表单内边距 */
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  width: 80%;
  /* 设置表单宽度 */
  margin: 0 auto;
  /* 水平居中 */

  .el-form-item__label {
    font-size: 20px;
    /* 标签字体大小 */
    margin-bottom: 10px;
    /* 标签下边距 */
    display: inline-block;
    /* 行内元素样式 */
    width: 40%;
    /* 设置标签宽度 */
  }

  .el-form-item__content {
    font-size: 18px;
    /* 内容字体大小 */
    margin-bottom: 20px;
    /* 内容下边距 */
    display: inline-block;
    /* 行内元素样式 */
    width: 50%;
    /* 设置内容宽度 */
  }

  .el-input {
    font-size: 16px;
    /* 输入框字体大小 */
    padding: 10px;
    /* 输入框内边距 */
    border-radius: 5px;
    /* 输入框边框圆角 */
    width: 80%;
    /* 输入框宽度 */
  }

  .el-radio-group {
    margin-top: 12px;
    /* 单选框组上边距 */
    font-size: 18px;
    /* 单选框字体大小 */
  }

  .custom-button {
    margin-top: 24px;
    /* 按钮上边距 */
    font-size: 18px;
    /* 按钮字体大小 */
    padding: 12px 24px;
    /* 按钮内边距 */
    border-radius: 5px;
    /* 按钮边框圆角 */
  }
}</style>

