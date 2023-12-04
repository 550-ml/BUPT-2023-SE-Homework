<template>
  <div class="w-full px-2 my-4">
    <div class="flex items-center justify-end mb-4 mr-4">
      <!-- 搜索框 -->
      <input
        type="text"
        placeholder="请输入房间号"
        class="p-2 border border-gray-300 rounded mr-2"
        v-model="searchTerm"
        @input="emitSearch"
      />
      <button class="bg-blue-500 text-white py-2 px-4 rounded" @click="executeSearch">搜索</button>
    </div>
    <!-- <table class="table-auto w-full rounded-lg shadow-md">
      <thead class="">
        <tr>
          <th>房间号</th>
          <th>状态</th>
          <th>入住时间</th>
          <th>退房时间</th>
          <th>总金额</th>
        </tr>
      </thead>
      <tbody>
        <RoomStates v-for="index in 4" :key="index" />
      </tbody>
    </table> -->
    <div v-if="deviceData" class="flex justify-center">
    <table class="border-collapse w-60 mt-8 shadow-md rounded-md overflow-hidden">
      <tbody>
        <tr v-for="(value, key) in deviceData" :key="key">
          <th class="border p-2 bg-gray-100">{{ key }}</th>
          <td class="border p-2">{{ value }}</td>
        </tr>
      </tbody>
    </table>
  </div>
    <div v-if="errorMessage" class="modal">
      <div class="modal-content">
        <p>{{ errorMessage }}</p>
        <button @click="closeModal" class="bg-blue-500 text-white py-2 px-4 rounded mt-4">关闭</button>
      </div>
    </div>
  </div>
</template>

<script>
import RoomStates from "../components/RoomStateHistory.vue";
import axios from "axios";

export default {
  components: {
    RoomStates
  },
  data() {
    return {
      searchTerm: "", // 用于存储搜索框的值
      deviceData: null
    };
  },
  methods: {
    executeSearch() {
      // if (!this.searchTerm) {
      //   // 搜索词为空时不发送请求
      //   return;
      // }

      // // 发送请求
      // axios
      //   .get(`/api/device/${this.searchTerm}`, {
      //     headers: {
      //       "X-CSRF-Token": "abcde12345" // 替换为你的CSRF token
      //     }
      //   })
      //   .then(response => {
      //     this.deviceData = response.data;
      //     if (!this.deviceData) {
      //       // 如果搜索结果为空，显示错误信息
      //       this.errorMessage = "未找到相关设备信息";
      //     }
      //   })
      //   .catch(error => {
      //     if (error.response && error.response.status === 401) {
      //       // 如果返回错误代码401，显示相应错误信息
      //       this.errorMessage = "未授权，请登录";
      //     } else {
      //       // 其他错误情况，显示默认错误信息
      //       console.error("请求失败", error);
      //       this.errorMessage = "请求失败，请重试"; // 根据实际情况设置错误信息
      //     }
      //   });
      this.deviceData = {
        room: "2-233",
        temperature: 26,
        wind_speed: 3,
        mode: "cold",
        sweep: true,
        is_on: true,
        last_update: "2023-09-18T11:45:14+08:00"
      };
    },
    closeModal() {
      // 关闭对话框
      this.errorMessage = null;
    }
  }
};
</script>
