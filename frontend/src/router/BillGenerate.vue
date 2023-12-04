<template>
  <div class="w-full px-2 my-4">
    <div class="flex items-center justify-between mb-4 mr-4">
      <div class="flex justify-start">
        <button @click="changeTab('tab1')" class="py-2 px-4 rounded cursor-pointer">
          <span class="">未入住房间</span>
        </button>
        <button @click="changeTab('tab2')" class="py-2 px-4 rounded cursor-pointer">
          <span class="">已入住房间</span>
        </button>
      </div>

      <div class="flex justify-end">
        <input
          type="text"
          placeholder="请输入房间号"
          class="p-2 border border-gray-300 rounded mr-2"
          v-model="searchTerm"
          @input="emitSearch"
        />
        <button class="bg-blue-500 text-white py-2 px-4 rounded" @click="executeSearch">搜索</button>
      </div>
    </div>

    <div v-if="deviceData">
      <div class="flex justify-center">
        <table class="border-collapse w-60 mt-8 shadow-md rounded-md overflow-hidden">
          <tbody>
            <tr v-for="(value, key) in deviceData" :key="key">
              <th class="border p-2 bg-gray-100">{{ key }}</th>
              <td class="border p-2">{{ value }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="flex justify-center items-center py-4 space-x-4">
        <button class="bg-blue-500 text-white py-2 px-4 rounded item-center" @click="openCheckOut">
          生成账单并退房
        </button>
        <button class="bg-blue-500 text-white py-2 px-4 rounded item-center" @click="openDetailedOrder">
          生成详单
        </button>
      </div>

      <div class="flex justify-center items-center py-4">
        <button class="bg-blue-500 text-white py-2 px-4 rounded item-center" @click="cancelSearch">返回列表</button>
      </div>
    </div>
    <div v-else>
      <div class="flex justify-center">
        <div v-if="activeTab === 'tab1'" class="mt-4">
          <table class="table-auto w-full rounded-lg shadow-md">
            <thead class="">
              <tr>
                <th>房间号</th>
              </tr>
            </thead>
            <tbody>
              <RoomStates v-for="index in 4" :key="index" />
            </tbody>
          </table>
        </div>
        <div v-else-if="activeTab === 'tab2'" class="mt-4">
          <table class="table-auto w-full rounded-lg shadow-md">
            <thead class="">
              <tr>
                <th>房间号</th>
                <th>入住时间</th>
                <th>总金额</th>
              </tr>
            </thead>
            <tbody>
              <RoomStates v-for="index in 4" :key="index" />
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-if="errorMessage" class="modal">
      <div class="modal-content">
        <p>{{ errorMessage }}</p>
        <button @click="closeModal" class="bg-blue-500 text-white py-2 px-4 rounded mt-4">关闭</button>
      </div>
    </div>
  </div>

  <div v-if="isCheckOutOpen" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
    <div class="bg-white p-6 rounded shadow-md">
      <!-- 对话框内容 -->
      <h2>xxx房间账单</h2>
      <button @click="closeCheckOut" class="mt-4 bg-blue-500 text-white py-2 px-4 rounded">关闭对话框</button>
    </div>
  </div>
  <div v-if="isDetailedOrderOpen" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
    <div class="bg-white p-6 rounded shadow-md">
      <!-- 对话框内容 -->
      <h2>xxx房间详单</h2>
      <button @click="closeDetailedOrder" class="mt-4 bg-blue-500 text-white py-2 px-4 rounded">关闭对话框</button>
    </div>
  </div>
</template>

<script>
import RoomStates from "../components/RoomState.vue";
import axios from "axios";

export default {
  components: {
    RoomStates
  },
  data() {
    return {
      searchTerm: "", // 用于存储搜索框的值
      deviceData: null,
      isCheckOutOpen: false,
      isDetailedOrderOpen: false,
      activeTab: "tab1"
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
    cancelSearch() {
      this.deviceData = null;
    },
    openCheckOut() {
      this.isCheckOutOpen = true;
    },
    closeCheckOut() {
      this.isCheckOutOpen = false;
    },
    openDetailedOrder() {
      this.isDetailedOrderOpen = true;
    },
    closeDetailedOrder() {
      this.isDetailedOrderOpen = false;
    },
    closeModal() {
      // 关闭对话框
      this.errorMessage = null;
    },
    changeTab(tab) {
      this.activeTab = tab;
    }
  }
};
</script>

<style scoped>
button span::after {
  content: "";
  display: block;
  width: 0;
  height: 2px;
  background-color: #3182ce;
  transition: width 0.1s ease;
}

button:hover span::after,
button:focus span::after {
  width: 100%;
}
</style>
