<!--
  文件名: AirConditionerManage.vue
  功能: 这个文件是用于管理空调的设置参数的界面。
  作者: 王拓
  创建日期: 2023-11-11
-->
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
                  <span class="border-head">{{ room.roomId }}</span>
                  <img src="../assets/room2.jpg" class="image" />

                  <div class="bottom">
                    <p>是否开启: <strong>{{ room.is_on }}</strong></p>
                    <p>空调模式: <strong>{{ room.mode }}</strong></p>
                    <p>当前风速: <strong>{{ room.speed }}</strong></p>
                    <p>当前温度: <strong>{{ room.currTemp }}</strong></p>
                    <p>目标温度: <strong>{{ room.targetTemp }}</strong></p>
                    <el-button class="button" :icon="Edit" plain @click="openDialog(room.roomId)">控制房间</el-button>
                  </div>

                </el-card>
                <el-dialog v-model="dialogVisible" title="设置空调状态" width="30%" :close-on-click-modal="false"
                  :close-on-press-escape="false">
                  <el-form ref="form" label-width="120px">
                    <el-form-item label="空调状态设置">
                      <el-radio-group v-model="startvalue" class="up_set_start">
                        <el-radio label="1" value="1" border class="start_text">开启</el-radio>
                        <el-radio label="0" value="0" border class="start_text">关闭</el-radio>
                      </el-radio-group>
                    </el-form-item>
                    <el-form-item label="目标温度(°C)" style="width: 353px;">
                      <el-input v-model="targetTemperature" type="number" placeholder="目标温度"></el-input>
                    </el-form-item>
                    <el-form-item label="风速设置" style="width: 500px;">
                      <el-select v-model="selectwindspeed" placeholder="风速选择" clearable>
                        <el-option label="低风速" value="1" />
                        <el-option label="中风速" value="2" />
                        <el-option label="高风速" value="3" />
                      </el-select>
                    </el-form-item>
                  </el-form>
                  <template #footer>
                    <span class="dialog-footer">
                      <el-button @click="dialogVisible = false">取消操作</el-button>
                      <el-button type="primary" @click="submitForm">确定发送</el-button>
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
                  <el-button type="primary" class="custom-button" @click="sendDataToBackend">
                    设置默认参数
                  </el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </el-main>
      </el-container>
      <el-footer>
        <el-button type="primary" @click="GetroomName">查询数据</el-button>
        <el-button type="primary" @click="stopFetching">停止查询</el-button>
      </el-footer>
    </el-container>
  </div>
</template>


<script lang="ts" setup>
import api from "../main.ts";
import { ref } from "vue";
import { ElMessage } from 'element-plus'
import { Edit } from '@element-plus/icons-vue'


const roomIds = ['test', '223', '224', '222', '223'];
let shouldFetchRoomInfo = true;
/**
 * @description 房间信息数组
 * @type {Array}
 */
const roomsInfo = ref([
  {
    roomId: roomIds[0],
    is_on: '未开启',
    mode: '未开启',
    speed: '未开启',
    currTemp: '未开启',
    targetTemp: '未开启',
  },
  {
    roomId: roomIds[0],
    is_on: '未开启',
    mode: '未开启',
    speed: '未开启',
    currTemp: '未开启',
    targetTemp: '未开启',
  },
  {
    roomId: roomIds[0],
    is_on: '未开启',
    mode: '未开启',
    speed: '未开启',
    currTemp: '未开启',
    targetTemp: '未开启',
  },
  {
    roomId: roomIds[0],
    is_on: '未开启',
    mode: '未开启',
    speed: '未开启',
    currTemp: '未开启',
    targetTemp: '未开启',
  },
  {
    roomId: roomIds[0],
    is_on: '未开启',
    mode: '未开启',
    speed: '未开启',
    currTemp: '未开启',
    targetTemp: '未开启',
  },
  {
    roomId: roomIds[0],
    is_on: '未开启',
    mode: '未开启',
    speed: '未开启',
    currTemp: '未开启',
    targetTemp: '未开启',
  }
])

/**
 * 异步获取房间信息
 * @param {string} roomId - 房间ID
 * 
 */
const fetchRoomInfo = async (roomId) => {
  try {
    const response = await api.get(`/status/${roomId}`);
    const roomData = response.data;

    // 根据接口返回的数据结构更新房间信息
    const updatedRooms = roomsInfo.value.map(room => {
      if (room.roomId === roomId) {
        if (roomData.is_on) {
          room.is_on = '已开启';
          room.mode = roomData.mode;
          if (roomData.wind_speed === 1) {
            room.speed = '低风速';
          } else if (roomData.wind_speed === 2) {
            room.speed = '中风速';
          } else if (roomData.wind_speed === 3) {
            room.speed = '高风速';
          } else {
            room.speed = '未知'; // 如果有其他风速选项，可以在这里处理
          }
          room.currTemp = `${roomData.temperature.toFixed(3)}°C`;
          room.targetTemp = `${roomData.target_temp.toFixed(3)}°C`;
        } else {
          room.is_on = '未开启';
          room.mode = '未开启';
          room.speed = '未开启';
          room.currTemp = `${roomData.temperature.toFixed(3)}°C`;
          room.targetTemp = `${roomData.target_temp.toFixed(3)}°C`;
        }
        return room;
      }
      return room;
    });
    roomsInfo.value = updatedRooms;

  } catch (error) {
    console.error('获取房间信息时出错:', error);
    GetroomName();
    ElMessage({
      message: `获取房间${roomId}信息时出错`,
      type: 'error',
    })
  }
};

/**
 * 异步获取房间名称和状态信息
 * 
 * 该函数用于发送异步 GET 请求获取房间的名称和状态信息，并更新房间的相关数据。
 * 
 * 函数执行的步骤包括：
 * 1. 发送 GET 请求获取房间状态信息
 * 2. 更新房间 ID 数组
 * 3. 更新房间信息数组
 * 4. 显示成功查询消息和房间加载成功消息
 * 
 * @returns {Promise<void>} 无返回值
 */
const GetroomName = async () => {
  const response = await api.get('/status');
  const responseData = response.data;
  ElMessage({
    message: `成功开始查询`,
    type: 'success',
  })
  // const responseData = [{ room: 'test1', is_on: 0 }, { room: 'test2', is_on: 0 }]
  console.log(responseData);
  roomIds.splice(0, roomIds.length, ...responseData.map(room => room.room));
  console.log(roomIds); // 输出更新后的 roomIds 数组
  roomsInfo.value = responseData.map(room => ({
    roomId: room.room,
    is_on: room.is_on === 0 ? '否' : '是',
    mode: '未开启',
    speed: '未开启',
    currTemp: '未开启',
    targetTemp: '未开启',
  }));
  console.log(roomsInfo.value);
  ElMessage({
    message: '房间加载成功',
    type: 'success',
  })
  shouldFetchRoomInfo = true;
  setInterval(() => {
    roomIds.forEach(roomId => {
      if (shouldFetchRoomInfo) {
        fetchRoomInfo(roomId);
      }
    });
  }, 3000);
};

/**
 * 停止获取房间信息
 */
const stopFetching = () => {
  shouldFetchRoomInfo = false;
  ElMessage({
    message: `成功停止查询`,
  })
};



// 控制某一个房间信息
const dialogVisible = ref(false);
const startvalue = ref('0'); // 初始化为默认值
const targetTemperature = ref('');
const selectwindspeed = ref('');
const selectedRoomId = ref('');

/**
 * 打开对话框
 * 
 * 该函数用于打开设置房间状态的对话框，并设置选中的房间 ID。
 * 
 * 函数执行的步骤包括：
 * 1. 设置选中的房间 ID
 * 2. 打开对话框
 * 3. 显示设置房间状态的消息
 * 
 * @param {string} roomId - 房间 ID
 * @returns {void} 无返回值
 */
const openDialog = (roomId) => {
  selectedRoomId.value = roomId;
  dialogVisible.value = true; // 打开对话框
  ElMessage({
    message: `设置${selectedRoomId.value}房间状态`,

  })
  console.log(selectedRoomId.value);
};

/**
 * 提交表单数据并发送请求
 * @function submitForm
 * @description 收集输入框中的数据，构建请求数据并发送POST请求到指定的API接口。
 * @returns {void}
 */
const submitForm = () => {
  // 收集输入框中的数据
  let dataToSend = {
    operation: "start, stop, temperature, wind_speed",
    data: `${startvalue.value}, ${startvalue.value === '1' ? '0' : '1'}, ${targetTemperature.value}, ${selectwindspeed.value}`
  };
  if (startvalue.value === '1') {

    dataToSend.data = '1,0,' + targetTemperature.value + ',' + selectwindspeed.value;
  } else {
    dataToSend.data = '0,1,' + targetTemperature.value + ',' + selectwindspeed.value;
  }
  const jsonData = JSON.stringify(dataToSend);
  console.log(jsonData);
  api.post(`/admin/devices/${selectedRoomId.value}`, jsonData)
    .then(response => {
      // 处理请求成功的响应
      ElMessage({
        message: '空调设置成功',
        type: 'success',
      })
      console.log('POST 请求成功:', response);
      // 这里可以根据返回的响应执行相应的逻辑
    })
    .catch(error => {
      // 处理请求错误
      ElMessage({
        message: '空调设置失败',
        type: 'error',
      })
      console.error('POST 请求出错:', error);
      // 这里可以根据错误执行相应的逻辑
    });
};


// 以下是中央空调设置
const radioValue = ref('cold'); // 初始化为默认值
const minTemperature = ref('');
const maxTemperature = ref('');
const defaultTemperature = ref('');
const rate = ref('');

/**
 * 发送数据到后端
 */
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

  // 使用 fetch 或 Axios 将数据发送到后端
  fetch('', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dataToSend)
  })
    .then(response => {
      // 处理来自后端的响应
      console.log('服务器返回的响应:', response);
    })
    .catch(error => {
      // 处理发送数据时的错误
      console.error('发送数据时出现错误:', error);
    });
}

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
  background: linear-gradient(to right, #d0dfed, #5a9be1);
  /* 添加渐变背景 */
  color: #ffffff;
  padding: 5px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid #0c3d6b;
  /* 添加底部边框 */
}

/* 定义head-text类的样式 */
.head-text {
  font-size: 60px;
  /* 增大字体大小 */
  font-weight: bold;
  text-shadow: 8px 8px 16px rgba(0, 0, 0, 0.7);
  /* 添加文字阴影 */
}

/* 左边那一栏文字 */
.el-tabs--left .el-tabs__item.is-left {
  font-size: 20px;
  /* 增大字体大小 */
  color: #17547c;
  /* 改变字体颜色 */
  font-family: 'Courier New', Courier, monospace;
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
  padding: 2px;
}

/* 主要内容样式 */
.show-mes {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin: 10px;
  padding: 0;
  justify-content: space-evenly;
}

.el-card {
  --el-card-padding: 5px;
  width: calc(31% - 5px);
  /* 调整卡片宽度 */
  height: auto;
  /* 自动调整卡片高度 */
  margin-bottom: 8px;
  border-radius: 25px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #dfedf5;
  transition: box-shadow 0.3s ease;
  padding: 10px;
  /* 调整内边距以减小卡片的总体高度 */
}

.el-card:hover {
  box-shadow: 0 50px 50px rgba(13, 88, 180, 0.15);
  /* 改变阴影效果 */
}

.border-head {
  color: #000000;
  /* 字体颜色 */
  border-radius: 17px;
  /* 圆角大小 */
  border: 2px solid #98bad0;
  /* 边框颜色和粗细 */
  background-color: rgb(243, 247, 248);
  /* 背景色 */
  padding: 5px 2px;
  /* 内边距 */
  font-size: 25px;
  /* 字体大小 */
  font-weight: 1000;
  /* 字体粗细 */
  font-family: ui-rounded, sans-serif;
  /* 字体 */
  display: flex;
  justify-content: center;
  /* 水平居中 */
  margin: 0 100px;
  /* 设置左右边距 */
  line-height: 1.1;
  /* 调整文字与边框的上下距离 */
  cursor: pointer;
}


/* 设置图片样式 */
.image {
  width: 72%;
  max-width: 100%;
  display: block;
  margin: 0 auto;
  margin-top: 7px;
  margin-bottom: 0px;
  border-radius: 20px 20px 10px 10px;
  /* 图片上方设置圆角 */
}

.show-mes .bottom {
  line-height: 1.5;
  font-size: 20px;
  color: #050505;
  font-family: 'Courier New', Courier, monospace;
  font-weight: 700;
  padding: 8px;
  margin-left: 25px;
  margin-top: 7px;
}

.show-mes .bottom p {
  margin: 2px 0;
  /* 增加段落间距 */
}

.show-mes .bottom p strong {
  font-weight: 700;
  /* 变量使用粗体 */
  color: #0e0e0e;
  /* 变量颜色 */
  font-family: fangsong;
  /* 使用不同字体 */

}

.button {
  padding: 10px 5px;
  /* 调整按钮内边距 */
  border-radius: 8px;
  /* 圆角大小 */
  background-color: #c1cedb;
  /* 背景颜色 */
  color: white;
  /* 字体颜色 */
  border: none;
  /* 移除边框 */
  font-size: 16px;
  /* 字体大小 */
  font-weight: 100;
  /* 字体粗细 */
  transition: background-color 0.3s ease;
  /* 添加背景颜色的过渡效果 */
  /* 背景色过渡效果 */
  cursor: pointer;
  /* 鼠标样式 */
  text-decoration: none;
  /* 移除链接默认下划线 */
}

.button:hover {
  background-color: #cdd3d9;
  /* 鼠标悬停时的背景色 */
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