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
                      <p>是否开启: {{ room.is_on }}</p>
                      <p>空调模式: {{ room.mode }}</p>
                      <p>当前风速: {{ room.speed }}</p>
                      <p>当前温度: {{ room.currTemp }}</p>
                      <p>目标温度: {{ room.targetTemp }}</p>
                      <p>服务时间: {{ room.servedTime }}</p>
                      <p>服务费用: {{ room.fee }}</p>
                      <el-button text class="button" @click="dialogVisible = true">操作</el-button>
                    </div>
                  </div>
                </el-card>
                <el-dialog v-model="dialogVisible" title="设置空调状态" width="30%" :before-close="handleClose">
                  <el-form ref="form" :model="form" label-width="120px">
                    <el-form-item label="操作">
                      <el-select v-model="form.operation" placeholder="请选择">
                        <el-option label="开始" value="start"></el-option>
                        <el-option label="停止" value="stop"></el-option>
                        <el-option label="温度" value="temperature"></el-option>
                        <el-option label="风速" value="wind_speed"></el-option>
                        <el-option label="模式" value="mode"></el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item label="数据">
                      <el-input v-model="form.data"></el-input>
                    </el-form-item>
                  </el-form>
                  <template #footer>
                    <span class="dialog-footer">
                      <el-button @click="dialogVisible = false">取消</el-button>
                      <el-button type="primary" @click="submitForm('form')">确定</el-button>
                    </span>
                  </template>
                </el-dialog>
              </div>
            </el-tab-pane>
            <el-tab-pane label="设置参数" class="left-text">
              <el-form label-width="200px" size="large" class="custom-form">
                <el-form-item label="默认模式">
                  <el-radio-group v-model="radioValue" class="select_hot_cold">
                    <el-radio label="hot" border class="hot_text">hot</el-radio>
                    <el-radio label="cold" border class="hot_text">cold</el-radio>
                  </el-radio-group>
                </el-form-item>

                <el-form-item label="最低温度">
                  <el-input v-model="minTemperature" type="number" placeholder="最低温度"></el-input>
                </el-form-item>

                <el-form-item label="最高温度">
                  <el-input v-model="maxTemperature" type="number" placeholder="最高温度"></el-input>
                </el-form-item>

                <el-form-item label="缺省温度">
                  <el-input v-model="defaultTemperature" type="number" placeholder="缺省温度"></el-input>
                </el-form-item>

                <el-form-item label="费率">
                  <el-input v-model="rate" type="number" placeholder="费率"></el-input>
                </el-form-item>

                <el-form-item>
                  <el-button type="primary" class="custom-button" @click="sendDataToBackend"> 设置默认参数 </el-button>
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
import { ElMessageBox } from "element-plus";
import axios from "axios";
const dialogVisible = ref(false);
const form = ref({
  operation: "",
  data: ""
});
const handleClose = (done: () => void) => {
  ElMessageBox.confirm("确定要关闭这个对话框吗？")
    .then(() => {
      done();
    })
    .catch(() => {
      // catch error
    });
};
const submitForm = async _formName => {
  const room = roomsInfo.value[0].roomId; // 你需要根据实际情况获取房间 ID
  try {
    const response = await axios.post(`/admin/devices/${room}`, {
      operation: form.value.operation,
      data: form.value.data
    });
    if (response.status === 200) {
      // 请求成功，处理响应数据
      // ...
    } else {
      // 请求失败，处理错误
      // ...
    }
  } catch (error) {
    // 网络错误，处理错误
    // ...
  }
};

const roomsInfo = ref([
  {
    roomId: "Room 1",
    is_on: "是",
    mode: "Cold",
    eed: "Medium",
    currTemp: "20°C",
    targetTemp: "接口没有",
    servedTime: "2 hours",
    fee: "$15"
  },
  {
    roomId: "Room 2",
    is_on: "是",
    mode: "Hot",
    speed: "High",
    currTemp: "30°C",
    targetTemp: "接口没有",
    servedTime: "3 hours",
    fee: "$20"
  },
  {
    roomId: "Room 2",
    is_on: "是",
    mode: "Hot",
    speed: "High",
    currTemp: "30°C",
    targetTemp: "接口没有",
    servedTime: "3 hours",
    fee: "$20"
  },
  {
    roomId: "Room 1",
    is_on: "是",
    mode: "Cold",
    speed: "Medium",
    currTemp: "20°C",
    targetTemp: "接口没有",
    servedTime: "2 hours",
    fee: "$15"
  },
  {
    roomId: "Room 1",
    is_on: "是",
    mode: "Cold",
    speed: "Medium",
    currTemp: "20°C",
    targetTemp: "接口没有",
    servedTime: "2 hours",
    fee: "$15"
  },
  {
    roomId: "Room 1",
    is_on: "是",
    mode: "Cold",
    speed: "Medium",
    currTemp: "20°C",
    targetTemp: "25°C",
    servedTime: "2 hours",
    fee: "$15"
  }
  // Add more rooms as needed...
]);
// 获取特定房间的信息
const fetchRoomInfo = async roomId => {
  try {
    // const sentData = {
    //   room: roomId
    // };
    // const jsonData = JSON.stringify(sentData);
    const response = await axios.get(`http://10.129.37.107:11451/api/status/${roomId}`);
    const roomData = response.data;

    // 根据接口返回的数据结构更新房间信息
    const updatedRooms = roomsInfo.value.map(room => {
      if (room.roomId === roomId) {
        if (roomData.is_on) {
          // 更新特定房间的信息
          room.mode = roomData.mode;
          room.speed = roomData.wind_speed;
          room.currTemp = `${roomData.temperature}°C`;
          // room.targetTemp = `${roomData.target_temperature}°C`;
          room.servedTime = roomData.served_time;
          // room.fee = roomData.fee;
          // 其他属性更新...
        } else {
          // 如果空调未开启，将所有值设为空值
          room.mode = "";
          room.speed = "";
          room.currTemp = "";
          // room.targetTemp = '';
          room.servedTime = "";
          // room.fee = '';
          // 其他属性更新...
        }
        return room;
      }
      return room;
    });

    // 将更新后的房间信息重新赋值给roomsInfo
    roomsInfo.value = updatedRooms;
  } catch (error) {
    console.error("获取房间信息时出错:", error);
    // 在这里处理错误，例如向用户显示错误消息
  }
};

// 假设你有一个包含所有房间ID的数组
const roomIds = ["222", "223", "224", "222", "223", "224"];
// 每秒获取所有房间的信息
setInterval(() => {
  roomIds.forEach(roomId => {
    fetchRoomInfo(roomId);
  });
}, 1000000000000000000000000000000000);

// This code keeps track of the current date and time
// const currentDate = ref(new Date());
// setInterval(() => {
//   currentDate.value = new Date();
// }, 1000);

const radioValue = ref("cold"); // 初始化为默认值
const minTemperature = ref("");
const maxTemperature = ref("");
const defaultTemperature = ref("");
const rate = ref("");
const sendDataToBackend = () => {
  // 收集输入框中的数据
  const dataToSend = {
    radioValue: radioValue.value, // 将 radioValue 加入发送的数据中
    minTemperature: minTemperature.value,
    maxTemperature: maxTemperature.value,
    defaultTemperature: defaultTemperature.value,
    rate: rate.value
    // 根据需要添加更多字段...
  };

  // 使用 fetch 或 Axios 将数据发送到后端（这是一个假设的函数）
  fetch("你的后端接口地址", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(dataToSend)
  })
    .then(response => {
      // 处理来自后端的响应
      console.log("服务器返回的响应:", response);
    })
    .catch(error => {
      // 处理发送数据时的错误
      console.error("发送数据时出现错误:", error);
    });
};
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
  height: fit-content;
  background: linear-gradient(to right, #67879c, #094073);
  /* 添加渐变背景 */
  color: #ffffff;
  padding: 10px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid #0c3d6b;
  /* 添加底部边框 */
}

/* 定义head-text类的样式 */
.head-text {
  font-size: 65px;
  /* 增大字体大小 */
  font-weight: bold;
  text-shadow: 8px 8px 16px rgba(0, 0, 0, 0.5);
  /* 添加文字阴影 */
}

/* 左边那一栏文字 */
.el-tabs--left .el-tabs__item.is-left {
  font-size: 30px;
  /* 增大字体大小 */
  color: #17547c;
  /* 改变字体颜色 */
  font-family: "Courier New", Courier, monospace;
  /* 改变字体 */
  font-weight: 700;
  /* 增大字重 */
  line-height: 1.8;
  /* 增大行高 */
  text-decoration: underline;
  /* 添加下划线装饰 */
  text-transform: capitalize;
  /* 将每个单词的首字母转换为大写 */
}

.el-tab-pane {
  padding: 20px;
}

/* 主要内容样式 */
.show-mes {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 0;
  /* 去除外边距 */
  padding: 0;
  /* 去除内边距 */
  justify-content: space-evenly;
}

.el-card {
  width: calc(30% - 20px);
  /* 调整卡片宽度 */
  height: auto;
  /* 自动调整卡片高度 */
  margin-bottom: 20px;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #cfdee7;
  transition: box-shadow 0.3s ease;
  padding: 10px;
  /* 调整内边距以减小卡片的总体高度 */
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
  line-height: 1.6;
  /* 增大行高 */
  font-size: 20px;
  /* 增大字体大小 */
  color: #050505;
  /* 改变字体颜色为白色 */
  font-family: "Courier New", Courier, monospace;
  /* 改变字体 */
  font-weight: 700;
  /* 增大字重 */
  text-align: left;
  /* 文字左对齐 */
  padding: 8px;
  /* 添加内边距 */
}

/* 按钮样式 */
.button {
  padding: 8px 8px;
  border-radius: 5px;
  background-color: #007bff;
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
  padding: 100px;
  /* 增加表单内边距 */
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  width: 80%;
  /* 设置表单宽度 */
  margin: 0 auto;
  /* 水平居中 */

  .el-form-item__label {
    font-size: 30px;
    /* 标签字体大小 */
    margin-bottom: 0px;
    /* 标签下边距 */
    display: inline-block;
    /* 行内元素样式 */
    width: 40%;
    /* 设置标签宽度 */
  }

  .el-form-item__content {
    font-size: 30px;
    /* 内容字体大小 */
    margin-bottom: 20px;
    /* 内容下边距 */
    display: inline-block;
    /* 行内元素样式 */
    width: 100%;
    /* 设置内容宽度 */
  }

  .el-input {
    font-size: 16px;
    /* 输入框字体大小 */
    padding: 10px;
    /* 输入框内边距 */
    border-radius: 5px;
    /* 输入框边框圆角 */
    width: 30%;
    /* 输入框宽度 */
  }

  .el-radio-group {
    margin-top: px;
    /* 单选框组上边距 */
    font-size: 30px;
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
}

.el-radio.is-bordered.el-radio--large .el-radio__label {
  font-size: 30px;
}
</style>
